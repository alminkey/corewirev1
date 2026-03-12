import { getHomepage } from "../lib/api";
import { buildSitemapEntries } from "../lib/seo";

export default async function sitemap() {
  const homepage = await getHomepage();
  return buildSitemapEntries(homepage);
}
