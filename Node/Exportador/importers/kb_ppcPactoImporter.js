import Monitoramento from "../models/kobo/monitoramento.model.js";
import ParcelaMonitoramento from "../models/kobo/parcela-monitoramento.model.js";
import SubparcelaMonitoramento from "../models/kobo/subparcela-monitoramento.model.js";
import {Op} from "sequelize";
import Especie from "#models/catalogo/especie.model.js";
import MonitoramentoEspecieNativa from "../models/kobo/monitoramento.especie.nativa.model.js";
import MonitoramentoEspecieInvasora from "../models/kobo/monitoramento.especie.invasora.model.js";
import Pessoa from "../models/pessoa/pessoa.model.js";
import PessoaFisica from "../models/pessoa/pessoa-fisica.model.js";
import PessoaJuridica from "../models/pessoa/pessoa-juridica.model.js";
import MonitoramentoMembro from "../models/kobo/membros.model.js";
import MidiaAdicionalParcela from "../models/kobo/midia.model.js";


/* ==========================================
   Helpers gerais
========================================== */
function mapPeriodo(valor) {
  if (!valor) return null;
  const v = String(valor).toLowerCase();
  if (v.includes("ano 0")) return "Ano_0";
  if (v.includes("ano 2,5")) return "Ano_2,5";
  if (v.includes("ano 5")) return "Ano_5";
  return null;
}

function parseBool(valor) {
  if (valor === null || valor === undefined) return false;
  const v = String(valor).trim().toLowerCase();
  return v.startsWith("s") || v === "true" || v === "1";
}

// XLSX → atributos do model Monitoramento
const monitoramentoMap = {
  "ID do Sítio": "idSitio",
  "Tipo do Sítio": "tipoSitio",
  "Selecione seu País": "pais",
  "Período de Amostragem": "periodoAmostragem",
  "Insira uma data": "dataColeta",
  "Hora de Início": "horaInicio",
  "Hora de Fim": "horaFim",
  "Observações": "observacoes",
};

/* ==========================================
   Pessoa / PessoaFisica (sem User)
========================================== */
const pessoaByNomeCache = new Map(); // nome lower → pessoa_id

/**
 * Procura/Cria cadeia correta SEM User:
 *  1) buscar PessoaFisica.nome ILIKE rawName → retorna pessoa_id
 *  2) se não houver, cria Pessoa e PessoaFisica(nome=rawName)
 * Retorna pessoa_id.
 */
/* ==========================================
   Pessoa / PessoaFisica (sem User, permite null)
========================================== */


  async function getOrCreatePessoaFisicaByNome(rawName) {
    if (!rawName) return null;
    const key = String(rawName).trim().toLowerCase();
    if (pessoaByNomeCache.has(key)) return pessoaByNomeCache.get(key);

    // tenta achar por PessoaFisica.nome
    const fisica = await PessoaFisica.findOne({
      where: { nome: { [Op.iLike]: rawName } },
      attributes: ["pessoa_id"],
    });

    if (fisica?.pessoa_id) {
      pessoaByNomeCache.set(key, fisica.pessoa_id);
      return fisica.pessoa_id;
    }

    // cria Pessoa + PessoaFisica
    const pessoa = await Pessoa.create({});
    await PessoaFisica.create({ pessoa_id: pessoa.id, nome: rawName });

    pessoaByNomeCache.set(key, pessoa.id);
    return pessoa.id;
  }

  async function getOrCreatePessoaJuridicaByNome(rawName) {
    const normalized = String(rawName || '').trim();
    if (!normalized) return null;

    const key = normalized.toLowerCase();
    if (pessoaByNomeCache.has(key)) return pessoaByNomeCache.get(key);

    const juridica = await PessoaJuridica.findOne({
      where: { razao_social: { [Op.iLike]: normalized } }, // match case-insensitive
      attributes: ['pessoa_id'],
    });

    if (juridica?.pessoa_id) {
      pessoaByNomeCache.set(key, juridica.pessoa_id);
      return juridica.pessoa_id;
    }

    const pessoa = await Pessoa.create({});
    await PessoaJuridica.create({ pessoa_id: pessoa.id, razao_social: normalized });

    pessoaByNomeCache.set(key, pessoa.id);
    return pessoa.id;
  }




/* ==========================================
   Espécies (parser + criação automática)
========================================== */
function splitSpeciesList(value) {
  if (!value) return [];
  return String(value)
    .split(/[,;]+/g)
    .map((s) => s.trim())
    .filter(Boolean);
}

function normalizeBinomial(scientific) {
  if (!scientific) return null;
  const tokens = String(scientific).trim().split(/\s+/);
  if (tokens.length < 2) return null;
  return `${tokens[0]} ${tokens[1]}`;
}

function extractPopularAndScientific(raw) {
  if (!raw) return { popular: null, scientific: null };
  const s = String(raw).trim();

  // Popular (Científico)
  const m = s.match(/^(.*?)\s*\(([^)]+)\)\s*$/);
  if (m && m[1] && m[2]) {
    const popular = m[1].trim();
    const sci = normalizeBinomial(m[2]);
    return { popular, scientific: sci };
  }

  // tenta achar "Genus species" no texto
  const mb = s.match(/\b([A-Z][a-z]+)\s+([a-z-]+)\b/);
  if (mb) {
    return { popular: null, scientific: normalizeBinomial(`${mb[1]} ${mb[2]}`) };
  }

  // sem binômio; trata como popular
  return { popular: s, scientific: null };
}

const especieCache = new Map(); // chave lower → especie_id

async function getOrCreateEspecieId(rawName) {
  if (!rawName) return null;
  const cacheKey = String(rawName).toLowerCase();
  if (especieCache.has(cacheKey)) return especieCache.get(cacheKey);

  const { popular, scientific } = extractPopularAndScientific(rawName);
  let found = null;

  // 1) tenta pelo nome científico
  if (scientific) {
    found = await Especie.findOne({
      where: {
        [Op.or]: [
          { nome_cientifico: { [Op.iLike]: scientific } },
          { nome_cientifico: { [Op.iLike]: `${scientific}%` } }, // com autores
        ],
      },
      attributes: ["id"],
    });

    if (!found) {
      const created = await Especie.create({
        nome_cientifico: scientific,
        nome: popular || null,
      });
      especieCache.set(cacheKey, created.id);
      return created.id;
    }
  }

  // 2) tenta pelo nome popular
  if (!found && popular) {
    found = await Especie.findOne({
      where: { nome: { [Op.iLike]: popular } },
      attributes: ["id"],
    });

    if (!found) {
      const created = await Especie.create({
        nome: popular,
        nome_cientifico: scientific || null,
      });
      especieCache.set(cacheKey, created.id);
      return created.id;
    }
  }

  const id = found ? found.id : null;
  especieCache.set(cacheKey, id);
  return id;
}

async function relacionarNativas(monitoramentoId, listStr) {
  const items = splitSpeciesList(listStr);
  if (!items.length) {
    console.log("   ↳ Nenhuma espécie nativa informada.");
    return { ok: 0, notFound: [] };
  }

  let ok = 0;
  const notFound = [];
  for (const item of items) {
    const especieId = await getOrCreateEspecieId(item);
    if (!especieId) { notFound.push(item); continue; }

    await MonitoramentoEspecieNativa.findOrCreate({
      where: { monitoramento_id: monitoramentoId, especie_id: especieId },
      defaults: { monitoramento_id: monitoramentoId, especie_id: especieId },
    });
    ok++;
  }
  return { ok, notFound };
}

async function relacionarInvasoras(monitoramentoId, listStr) {
  const items = splitSpeciesList(listStr);
  if (!items.length) {
    console.log("   ↳ Nenhuma espécie invasora informada.");
    return { ok: 0, notFound: [] };
  }

  let ok = 0;
  const notFound = [];
  for (const item of items) {
    const especieId = await getOrCreateEspecieId(item);
    if (!especieId) { notFound.push(item); continue; }

    await MonitoramentoEspecieInvasora.findOrCreate({
      where: { monitoramento_id: monitoramentoId, especie_id: especieId },
      defaults: { monitoramento_id: monitoramentoId, especie_id: especieId },
    });
    ok++;
  }
  return { ok, notFound };
}

/* ==========================================
   Importer principal
========================================== */
export async function kb_importPPC_Pacto_CERT(rows = []) {
  try {
    console.log(`🔍 Importando ${rows.length} registros de PPC_Pacto_CERT...`);

    for (const [i, row] of rows.entries()) {
      try {
       
        /* ===== 0) Pessoa (Responsável pela Coleta) ===== */
        const responsavelNome = row["Nome do Responsável pela Coleta"];
        let responsavelColetaId = null;
        const organizacaoNome = row["Nome da Organização"];
        let organizacaoId = null;

        if (organizacaoNome && String(organizacaoNome).trim()) {
          organizacaoId = await getOrCreatePessoaJuridicaByNome(organizacaoNome);
        } else {
          organizacaoId = null;
        }

        if (responsavelNome && String(responsavelNome).trim()) {
          responsavelColetaId = await getOrCreatePessoaFisicaByNome(responsavelNome);
        } else {
          responsavelColetaId = null; // agora pode ficar null sem erro
        }

        /* ===== 1) MONITORAMENTO ===== */
        const monitoramentoData = {};
        for (const [coluna, campo] of Object.entries(monitoramentoMap)) {
          monitoramentoData[campo] = row[coluna] ?? null;
        }
        monitoramentoData.periodoAmostragem = mapPeriodo(row["Período de Amostragem"]);
        monitoramentoData.responsavelColetaId = responsavelColetaId;
        monitoramentoData.organizacaoId = organizacaoId;

        // _uuid da planilha
        const uuidFromSheetRaw = row["_uuid"];
        const uuidFromSheet = uuidFromSheetRaw && String(uuidFromSheetRaw).trim().toLowerCase();

        // Validação simples de formato UUID v4 (evita "invalid input syntax for type uuid")
        const UUID_V4_RX = /^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i;
        const hasValidUuid = !!(uuidFromSheet && UUID_V4_RX.test(uuidFromSheet));

        let monitoramento = null;

        if (hasValidUuid) {
          // ✅ Igualdade direta para coluna UUID
          monitoramento = await Monitoramento.findOne({
            where: { uuid: uuidFromSheet }, // nada de Op.iLike aqui
            attributes: ["id", "uuid"],
          });

          if (monitoramento) {
            console.log(`   ↔️ Monitoramento já existe para uuid=${uuidFromSheet}. Reutilizando.`);
          }
        } else if (uuidFromSheet) {
          console.warn(`   ⚠️ _uuid com formato inválido: "${uuidFromSheet}". Ignorando como chave.`);
        }

        // Cria se não encontrou (ou se não veio uuid válido)
        if (!monitoramento) {
          const payload = { ...monitoramentoData };
          if (hasValidUuid) payload.uuid = uuidFromSheet; // banco aceita direto porque é UUID válido

          monitoramento = await Monitoramento.create(payload);
          console.log(
            hasValidUuid
              ? `   ✅ Monitoramento criado com uuid=${uuidFromSheet}.`
              : `   ✅ Monitoramento criado (uuid gerado automaticamente).`
          );
        }


        // vincula também na tabela de membros (sempre que houver pessoa)
        if (responsavelColetaId) {
          await MonitoramentoMembro.findOrCreate({
            where: {
              monitoramento_id: monitoramento.id,
              pessoa_id: responsavelColetaId,
            },
            defaults: {
              monitoramento_id: monitoramento.id,
              pessoa_id: responsavelColetaId,
              funcao: "Responsável pela coleta",
            },
          });
        }
        if (organizacaoId) {
          await MonitoramentoMembro.findOrCreate({
            where: {
              monitoramento_id: monitoramento.id,
              pessoa_id: organizacaoId,
            },
            defaults: {
              monitoramento_id: monitoramento.id,
              pessoa_id: organizacaoId,
              funcao: "Responsável pela coleta",
            },
          });
        }
        

        /* ===== 1.1) ESPÉCIES ===== */
        const campoNativas =
          "Indicador 2.1: Identificação de espécies nativas plantadas de recobrimento";
        const campoInvasoras = "Indicador 2.2. Espécies invasoras arbóreas";

        const nativasStr = row[campoNativas];
        const invasorasStr = row[campoInvasoras];

        if (nativasStr) {
          const { ok, notFound } = await relacionarNativas(monitoramento.id, nativasStr);
          console.log(`   ↳ Nativas relacionadas: ${ok}`);
          if (notFound.length)
            console.warn(`   ⚠️ Nativas não encontradas/criadas (linha ${i + 1}): ${notFound.join(" | ")}`);
        } else {
          console.log("   ↳ Nenhuma espécie nativa informada.");
        }

        if (invasorasStr) {
          const { ok, notFound } = await relacionarInvasoras(monitoramento.id, invasorasStr);
          console.log(`   ↳ Invasoras relacionadas: ${ok}`);
          if (notFound.length)
            console.warn(`   ⚠️ Invasoras não encontradas/criadas (linha ${i + 1}): ${notFound.join(" | ")}`);
        } else {
          console.log("   ↳ Nenhuma espécie invasora informada.");
        }

        /* ===== 2) PARCELA ===== */
        const [parcela] = await ParcelaMonitoramento.findOrCreate({
          where: {
            idParcela: row["Identificação (ID) da Parcela de Monitoramento de Árvores"],
          },
          defaults: {
            estrato: row["Estrato"],
            tipoParcela: row["Tipo de Parcela"],
            descricaoEspacamentoPlantio:
              row["Descrição do espaçamento de plantio dentro da parcela"],
            numeroReamostragens:
              row["Número de Reamostragens Necessárias para Parcelas 30m x 30m"],
            arvoresDAPPresentes: parseBool(
              row["Há árvores >10cm DAP presentes na parcela?"]
            ),
            monitoramentoId: monitoramento.id,
            vertices: [
              {
                lat: row["_Vertice 1 da parcela de 30m x 30m_latitude"],
                lon: row["_Vertice 1 da parcela de 30m x 30m_longitude"],
                alt: row["_Vertice 1 da parcela de 30m x 30m_altitude"],
                precisao: row["_Vertice 1 da parcela de 30m x 30m_precision"],
              },
              {
                lat: row["_Vertice 2 da parcela de 30m x 30m_latitude"],
                lon: row["_Vertice 2 da parcela de 30m x 30m_longitude"],
                alt: row["_Vertice 2 da parcela de 30m x 30m_altitude"],
                precisao: row["_Vertice 2 da parcela de 30m x 30m_precision"],
              },
              {
                lat: row["_Vertice 3 da parcela de 30m x 30m_latitude"],
                lon: row["_Vertice 3 da parcela de 30m x 30m_longitude"],
                alt: row["_Vertice 3 da parcela de 30m x 30m_altitude"],
                precisao: row["_Vertice 3 da parcela de 30m x 30m_precision"],
              },
              {
                lat: row["_Vertice 4 da parcela de 30m x 30m_latitude"],
                lon: row["_Vertice 4 da parcela de 30m x 30m_longitude"],
                alt: row["_Vertice 4 da parcela de 30m x 30m_altitude"],
                precisao: row["_Vertice 4 da parcela de 30m x 30m_precision"],
              },
            ],
          },
        });

        /* ===== 3) SUBPARCELA ===== */
        const lat = row["_Centróide da subparcela de 3m x 3m_latitude"];
        const lon = row["_Centróide da subparcela de 3m x 3m_longitude"];

        if (lat && lon) {
          const [subparcela] = await SubparcelaMonitoramento.findOrCreate({
            where: { idSubparcela: `SP-${i + 1}`, parcelaId: parcela.id },
            defaults: {
              centroideLatitude: lat,
              centroideLongitude: lon,
              centroideAltitude: row["_Centróide da subparcela de 3m x 3m_altitude"],
              centroidePrecisao: row["_Centróide da subparcela de 3m x 3m_precision"],
              fotoUrl: row["Foto da subparcela 3mx3m_URL"],
              descricaoLocalizacao:
                row[
                  "Descrição da localização da subparcela (3mx3m) dentro da parcela maior (30mx30m)"
                ],
              numeroAmostragens:
                row["**Número de amostragens necessárias para a parcela de 3m x 3m**"],
              arvoresDAP_1_9_Presentes: parseBool(
                row["**Existem árvores de 1-9,9cm DAP na parcela de 3m x 3m?**"]
              ),
            },
          });

          console.log(
            subparcela?._options?.isNewRecord
              ? `   ↳ Subparcela criada (linha ${i + 1})`
              : `   ↔️ Subparcela já existia (linha ${i + 1})`
          );
        } else {
          console.log(`   ⚠️ Nenhuma subparcela encontrada (linha ${i + 1}), ignorando...`);
        }

        /* ===== 4) Midia Adicional ===== */
        function cleanStr(x) {
          const s = (x ?? '').toString().trim();
          return s.length ? s : null;
        }

        // Mapeia todos os campos "Foto do vertice" (30x30 e 30x15)
        function collectVertexPhotos(row) {
          const entries = [];

          // 30m x 30m — chaves sem sufixo
          for (let i = 1; i <= 4; i++) {
            const nomeKey = `Foto do vertice ${i}`;
            const urlKey  = `Foto do vertice ${i}_URL`;
            const nome = cleanStr(row[nomeKey]);
            const url  = cleanStr(row[urlKey]);
            if (nome || url) entries.push({ fotoNome: nome, fotoUrl: url });
          }

          // 30m x 15m — chaves com sufixo "_1" (quando existirem)
          for (let i = 1; i <= 4; i++) {
            const nomeKey = `Foto do vertice ${i}_1`;
            const urlKey  = `Foto do vertice ${i}_URL_1`;
            const nome = cleanStr(row[nomeKey]);
            const url  = cleanStr(row[urlKey]);
            if (nome || url) entries.push({ fotoNome: nome, fotoUrl: url });
          }

          return entries;
        }

        async function saveMidiasAdicionaisParcela(parcelaId, row) {
          const items = collectVertexPhotos(row);
          if (!items.length) return 0;

          let created = 0;
          // evita duplicar: usa findOrCreate por (parcelaId, fotoNome, fotoUrl)
          for (const it of items) {
            await MidiaAdicionalParcela.findOrCreate({
              where: {
                parcelaId,
                fotoNome: it.fotoNome ?? null,
                fotoUrl: it.fotoUrl ?? null, // envia null se vazio p/ não quebrar isUrl
              },
              defaults: {
                parcelaId,
                fotoNome: it.fotoNome ?? null,
                fotoUrl: it.fotoUrl ?? null,
              },
            });
            created++;
          }
          return created;
        }

        // salvar mídias adicionais de vértices da PARCELA
        const qntMidias = await saveMidiasAdicionaisParcela(parcela.id, row);
        if (qntMidias) {
          console.log(`   ↳ Mídias adicionais (vértices) salvas: ${qntMidias}`);
        } else {
          console.log("   ↳ Nenhuma mídia adicional de vértice encontrada.");
        }


        console.log(`✅ Registro ${i + 1} importado.`);
      } catch (err) {
        console.error(`❌ Erro na linha ${i + 1}:`, {
          name: err.name,
          message: err.message,
          details: err.errors ? err.errors.map((e) => e.message) : null,
          row,
        });
      }
    }

    console.log(`🏁 Importação PPC_Pacto_CERT concluída: ${rows.length} registros`);
  } catch (err) {
    console.error("❌ Erro ao importar PPC_Pacto_CERT:", err);
  }
}
