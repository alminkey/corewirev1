"use server";

import { redirect } from "next/navigation";

import {
  archiveAdminDraft,
  createAdminDraft,
  publishAdminDraft,
  updateProgrammingSettings,
  updateAdminDraft,
} from "../../lib/api";
import type { ProgrammingSettings } from "../../lib/types";


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

function parseBooleanField(formData: FormData, key: string) {
  return formData.get(key) === "on";
}

export async function applyProgrammingSettingsAction(formData: FormData) {
  const topicCount = Number(formData.get("topic-count") ?? 0);
  const intervalCount = Number(formData.get("interval-count") ?? 0);
  const windowCount = Number(formData.get("window-count") ?? 0);

  const payload: ProgrammingSettings = {
    topics: Array.from({ length: topicCount }, (_, index) => ({
      name: String(formData.get(`topic-name-${index}`) ?? "").trim(),
      enabled: parseBooleanField(formData, `topic-enabled-${index}`),
    })).filter((topic) => topic.name),
    intervals: Array.from({ length: intervalCount }, (_, index) => ({
      label: String(formData.get(`interval-label-${index}`) ?? "").trim(),
      minutes: Number(formData.get(`interval-minutes-${index}`) ?? 0),
      enabled: parseBooleanField(formData, `interval-enabled-${index}`),
    })).filter((interval) => interval.label && interval.minutes > 0),
    schedule_windows: Array.from({ length: windowCount }, (_, index) => ({
      label: String(formData.get(`window-label-${index}`) ?? "").trim(),
      start_hour: Number(formData.get(`window-start-${index}`) ?? 0),
      end_hour: Number(formData.get(`window-end-${index}`) ?? 0),
      timezone: String(formData.get(`window-timezone-${index}`) ?? "").trim(),
      enabled: parseBooleanField(formData, `window-enabled-${index}`),
    })).filter((window) => window.label && window.timezone),
  };

  await updateProgrammingSettings(payload);
  redirect("/admin#programming-controls");
}
