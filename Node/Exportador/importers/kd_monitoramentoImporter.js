import Monitoramento from "../models/kobo/monitoramento.model.js";
import { normalizeKeys } from "../utils/normalizeKeys.js";

export async function kb_importMonitoramento(file) {
  try {
    const rowsBySheet = import_xlsx({ filePath: file });
    const rows = normalizeKeys(rowsBySheet["PPC_Pacto_CERT"] || []);

    for (const row of rows) {
      await Monitoramento.create({
        idSitio: row["id_do_sitio"],
        tipoSitio: row["tipo_do_sitio"],
        pais: row["selecione_seu_pais"],
        periodoAmostragem: row["periodo_de_amostragem"],
        dataColeta: row["insira_uma_data"],
        horaInicio: row["hora_de_inicio"],
        horaFim: row["hora_de_fim"],
        coberturaCopaPct: row["indicador_11_cobertura_de_copa_pct"],
        invasorasNivel: row["indicador_12_nivel_de_invasoras"],
        compactacaoSoloConstatada: row["indicador_32_compactacao_do_solo"],
        conservacaoSoloErosao: row["indicador_331_conservacao_do_solo_erosao"],
        conservacaoSoloSoloDescoberto: row["indicador_332_conservacao_do_solo_solo_descoberto"],
        filtrosEdaficosOutros: row["indicador_34_outros_filtros_edaficos"],
        fogoOcorrencia: row["indicador_41_ocorrencia_de_fogo"],
        fogoFotoUrl: row["indicador_41_foto_url"],
        gadoPresenca: row["indicador_42_presenca_de_gado"],
        ataqueFormigas: row["indicador_43_ataque_de_formigas"],
        observacoes: row["observacoes"],
        status: row["_status"] || "submitted_via_web",
        submission_time: row["_submission_time"],
        submittedById: null, // precisa mapear externamente
        version: row["__version__"]
      });
    }
    console.log(`✅ Monitoramento importado: ${rows.length} registros`);
  } catch (err) {
    console.error("❌ Erro ao importar Monitoramento:", err);
  }
}
