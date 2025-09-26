import fs from "fs";
import path from "path";
import TMSitio from "../models/terramatch/sitio/tm-sitio.model.js";
import TMGeometriaSitio from "../models/terramatch/sitio/tm-geometria-sitio.model.js";

/**
 * Importa um GeoJSON de sítio para a tabela tm_geometria_sitio
 * @param {string} filePath - Caminho do arquivo .geojson
 */
export async function importGeometriaSitio(filePath) {
  try {
    const raw = fs.readFileSync(filePath, "utf-8");
    const geojson = JSON.parse(raw);

    if (!geojson.features || geojson.features.length === 0) {
      console.warn(`⚠️ GeoJSON vazio: ${filePath}`);
      return;
    }

    for (const feature of geojson.features) {
      const nomeSitio =
        feature.properties?.name ||
        feature.properties?.nome ||
        feature.properties?.SiteName ||
        feature.properties?.Site;
       

      const geometry = feature.geometry;

      if (!nomeSitio) {
        console.warn(`⚠️ Feature sem nome no arquivo ${filePath}`);
        continue;
      }

      // busca o sítio pelo nome
      const sitio = await TMSitio.findOne({ where: { nome: nomeSitio } });
      if (!sitio) {
        console.warn(`⚠️ Sítio não encontrado para nome "${nomeSitio}" (arquivo ${filePath})`);
        continue;
      }

      await TMGeometriaSitio.create({
        nome_arquivo: path.basename(filePath),
        tipo_geometria: geometry.type,
        geometria: geometry, // Sequelize/PostGIS aceita objeto GeoJSON aqui
        tm_sitio_id: sitio.id
      });

      console.log(`✅ Geometria importada para sítio: ${nomeSitio} (id: ${sitio.id})`);
    }
  } catch (err) {
    console.error(`❌ Erro ao importar GeoJSON ${filePath}:`, err);
  }
}
