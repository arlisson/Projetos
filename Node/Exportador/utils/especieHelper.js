// utils/especie.helper.js
import { Op } from "sequelize";
import Especie from "#models/catalogo/especie.model.js";

// cache simples para acelerar buscas repetidas durante o ETL
const especieCache = new Map(); // chave: raw lower → id (ou null)

/** Normaliza um binômio científico para "Genus species" (sem autores). */
function normalizeBinomial(scientific) {
  if (!scientific) return null;
  const tokens = String(scientific).trim().split(/\s+/);
  if (tokens.length < 2) return null;
  return `${tokens[0]} ${tokens[1]}`;
}

/**
 * Extrai (popular, scientific) de uma string.
 * Aceita formatos:
 *  - "Popular (Genus species ...)"
 *  - "Genus species" em qualquer lugar da string
 *  - "Popular" puro (sem binômio)
 */
function extractPopularAndScientific(raw) {
  if (!raw) return { popular: null, scientific: null };
  const s = String(raw).trim();

  // Caso "Popular (Genus species ...)"
  const m = s.match(/^(.*?)\s*\(([^)]+)\)\s*$/);
  if (m && m[1] && m[2]) {
    const popular = m[1].trim();
    const sci = normalizeBinomial(m[2]);
    return { popular, scientific: sci };
  }

  // Captura um binômio presente em qualquer lugar
  const mb = s.match(/\b([A-Z][a-z]+)\s+([a-z-]+)\b/);
  if (mb) {
    return { popular: null, scientific: normalizeBinomial(`${mb[1]} ${mb[2]}`) };
  }

  // Sem binômio; trata tudo como nome popular
  return { popular: s, scientific: null };
}

/**
 * Busca/cria uma Especie e retorna seu id.
 * @param {string} rawName - nome tal como veio (popular, científico ou "Popular (Científico)")
 * @param {object} [options]
 * @param {import('sequelize').Transaction} [options.transaction]
 * @returns {Promise<number|null>}
 */
export async function getOrCreateEspecieId(rawName, options = {}) {
  if (!rawName) return null;
  const { transaction } = options;

  const cacheKey = String(rawName).toLowerCase();
  if (especieCache.has(cacheKey)) return especieCache.get(cacheKey);

  const { popular, scientific } = extractPopularAndScientific(rawName);
  let found = null;

  // 1) tenta pelo nome científico (exato ou iniciando — para cobrir autores)
  if (scientific) {
    found = await Especie.findOne({
      where: {
        [Op.or]: [
          { nome_cientifico: { [Op.iLike]: scientific } },
          { nome_cientifico: { [Op.iLike]: `${scientific}%` } }, // com autores
        ],
      },
      attributes: ["id"],
      transaction,
    });

    if (found) {
      especieCache.set(cacheKey, found.id);
      return found.id;
    }
  }

  // 2) tenta pelo nome popular
  if (popular) {
    found = await Especie.findOne({
      where: { nome: { [Op.iLike]: popular } },
      attributes: ["id"],
      transaction,
    });

    if (found) {
      especieCache.set(cacheKey, found.id);
      return found.id;
    }
  }

  // 3) criar
  const created = await Especie.create(
    {
      nome: popular || null,
      nome_cientifico: scientific || null,
    },
    { transaction }
  );

  especieCache.set(cacheKey, created.id);
  return created.id;
}

export default getOrCreateEspecieId;
