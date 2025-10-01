import SubparcelaMonitoramento from "../models/kobo/subparcela-monitoramento.model.js";
import { normalizeKeys } from "../utils/normalizeKeys.js";

export async function kb_importSubParcelaMonitoramento(file) {
  try {
    const rowsBySheet = import_xlsx({ filePath: file });
    const rows = normalizeKeys(rowsBySheet["PPC_Pacto_CERT"] || []);

    for (const [i, row] of rows.entries()) {
      await SubparcelaMonitoramento.create({
        idSubparcela: `SP-${i+1}`, // 👈 gerado, já que não vem no XLSX
        centroideLatitude: row["subparcela_lat"],
        centroideLongitude: row["subparcela_lon"],
        centroideAltitude: row["subparcela_alt"],
        centroidePrecisao: row["subparcela_prec"],
        fotoUrl: row["subparcela_foto_url"],
        descricaoLocalizacao: row["descricao_localizacao"],
        numeroAmostragens: row["numero_amostragens_3x3"],
        arvoresDAP_1_9_Presentes: row["arvores_dap_1_9_presentes"]
      });
    }
    console.log(`✅ Subparcelas importadas: ${rows.length}`);
  } catch (err) {
    console.error("❌ Erro ao importar Subparcelas:", err);
  }
}
