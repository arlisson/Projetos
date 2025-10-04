// import {import_csv, import_xlsx} from "./funcoes.js";


// import_csv({filePath:"../Arli/TerraMatch/projects-MDPS - Flagship/site reports/MDPS - Flagship - Sítio 1 - Fazenda Ferro Estrela (CI 2) - site reports.csv", separator:",", export_json:true});

// // import_xlsx({filePath:"../PlanilhasAndre/10.21.2024 Project and site reports TM.xlsx",export_json:true});

import { importFiles } from "./importFiles.js";

const files = [
  "../Arli/TerraMatch/projects-MDPS - Flagship/MDPS - Flagship - project establishment data.csv",
  "../Arli/TerraMatch/projects-MDPS - Flagship/MDPS - Flagship - site establishment data.csv",
  "../Arli/TerraMatch/projects-MDPS - Flagship/Sites Shapefiles/Sítio 1 (Fazenda Álamo).geojson",
  "../Arli/TerraMatch/projects-MDPS - Flagship/MDPS - Flagship - project reports.csv",
  "../Arli/TerraMatch/projects-MDPS - Flagship/site reports/MDPS - Flagship - Sítio 1 (Fazenda Álamo) - site reports.csv",
   "../Arli/Kobo/CERT_Database_MonitoringY0_CBCA01_02.xlsx",
  "../Arli/Kobo/PPCPACTO_Tree_Monitoring_-_Brazil_only_-_all_versions_-_Portuguese_pt_-_2024-11-08-13-36-52 (1).xlsx"
];

// const files = [
//   "../Arli/Kobo/CERT_Database_MonitoringY0_CBCA01_02.xlsx",
// ];

await importFiles(files);

