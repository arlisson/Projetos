import ParcelaMonitoramento from "../models/kobo/parcela-monitoramento.model.js";
import { normalizeKeys } from "../utils/normalizeKeys.js";

export async function kb_importParcelaMonitoramento(file) {
  try {
    const rowsBySheet = import_xlsx({ filePath: file });
    const rows = normalizeKeys(rowsBySheet["PPC_Pacto_CERT"] || []);

    for (const row of rows) {
      await ParcelaMonitoramento.create({
        idParcela: row["id_parcela_monitoramento"],
        estrato: row["estrato"],
        tipoParcela: row["tipo_parcela"],
        descricaoEspacamentoPlantio: row["descricao_espacamento_plantio"],
        numeroReamostragens: row["numero_reamostragens"],
        arvoresDAPPresentes: row["arvores_dap_maior10"],
        vertices: [
          { lat: row["vertice1_lat"], lon: row["vertice1_lon"], alt: row["vertice1_alt"], precisao: row["vertice1_prec"] },
          { lat: row["vertice2_lat"], lon: row["vertice2_lon"], alt: row["vertice2_alt"], precisao: row["vertice2_prec"] },
          { lat: row["vertice3_lat"], lon: row["vertice3_lon"], alt: row["vertice3_alt"], precisao: row["vertice3_prec"] },
          { lat: row["vertice4_lat"], lon: row["vertice4_lon"], alt: row["vertice4_alt"], precisao: row["vertice4_prec"] },
        ]
      });
    }
    console.log(`✅ Parcelas importadas: ${rows.length}`);
  } catch (err) {
    console.error("❌ Erro ao importar Parcelas:", err);
  }
}
