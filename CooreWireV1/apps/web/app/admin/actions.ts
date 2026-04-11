"use server";

import { redirect } from "next/navigation";

import {
  archiveAdminDraft,
  createAdminDraft,
  publishAdminDraft,
  updateAdminDraft,
} from "../../lib/api";


function parseDraftForm(formData: FormData) {
  return {
    id: String(formData.get("id") ?? "").trim(),
    headline: String(formData.get("headline") ?? "").trim(),
    dek: String(formData.get("dek") ?? "").trim(),
    slug: String(formData.get("slug") ?? "").trim(),
    body: String(formData.get("body") ?? "").trim(),
    tags: String(formData.get("tags") ?? "")
      .split(",")
      .map((value) => value.trim())
      .filter(Boolean),
  };
}

export async function saveOwnerDraftAction(formData: FormData) {
  const payload = parseDraftForm(formData);

  if (!payload.headline || !payload.slug) {
    throw new Error("Headline and slug are required");
  }

  const draft = payload.id
    ? await updateAdminDraft(payload.id, payload)
    : await createAdminDraft(payload);

  redirect(`/admin?draft=${draft.id}`);
}

export async function publishOwnerDraftAction(formData: FormData) {
  const payload = parseDraftForm(formData);

  if (!payload.headline || !payload.slug) {
    throw new Error("Headline and slug are required");
  }

  const draft = payload.id
    ? await updateAdminDraft(payload.id, payload)
    : await createAdminDraft(payload);

  await publishAdminDraft(draft.id);
  redirect(`/admin?draft=${draft.id}`);
}

export async function archiveOwnerDraftAction(formData: FormData) {
  const payload = parseDraftForm(formData);

  if (!payload.id) {
    throw new Error("Draft id is required");
  }

  await archiveAdminDraft(payload.id);
  redirect(`/admin?draft=${payload.id}`);
}
