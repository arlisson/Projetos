import TMProjeto from "../models/terramatch/projeto/tm-projeto.model.js";

/**
 * Normaliza dados de sítios garantindo que cada um
 * tenha um `project_uuid` válido para vincular ao projeto.
 *
 * @param {Array} sitios - Array de objetos vindos do CSV/XLSX
 * @returns {Array} - Array com os sítios normalizados
 */
export async function normalizeSitesData(sitios) {
  // carrega todos os projetos já existentes no banco
  const projetos = await TMProjeto.findAll({ raw: true });

  // cria um mapa nome -> uuid para fallback
  const mapByName = {};
  projetos.forEach((p) => {
    if (p.nome) {
      mapByName[p.nome.trim()] = p.uuid;
    }
  });

  // normaliza cada registro de sítio
  return sitios.map((s) => {
    let projectUuid =
      s.project_uuid ||
      s["project-uuid"] ||
      s.projectUuid ||
      null;

    // se não veio o uuid no arquivo, tenta pelo nome do projeto
    if (!projectUuid && s.project_name && mapByName[s.project_name.trim()]) {
      projectUuid = mapByName[s.project_name.trim()];
    }

    return {
      ...s,
      project_uuid: projectUuid,
    };
  });
}
