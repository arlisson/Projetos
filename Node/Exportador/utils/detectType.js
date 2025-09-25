export function detectFileType(data) {
  if (!Array.isArray(data) || data.length === 0) return null;
  const keys = Object.keys(data[0]);

  // Project establishment
  if (keys.includes("project_name") && keys.includes("organization-name") && keys.includes("trees_grown_goal")) {
    return "project_establishment";
  }

  // Site establishment
  if (keys.includes("site-name") && keys.includes("restoration_strategy") && keys.includes("land_use_types")) {
    return "site_establishment";
  }

  // Project reports
  if (keys.includes("project_uuid") && keys.includes("technical_narrative") && keys.includes("title")) {
    return "project_report";
  }

  // Site reports
  if (keys.includes("site-id") && keys.includes("site-name") && keys.includes("technical_narrative")) {
    return "site_report";
  }

  return null;
}
