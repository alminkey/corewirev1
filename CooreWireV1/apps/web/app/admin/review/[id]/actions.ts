"use server";

import { redirect } from "next/navigation";

import { postReviewDecision } from "../../../../lib/api";


export async function submitReviewDecision(formData: FormData) {
  const id = String(formData.get("id") ?? "");
  const action = String(formData.get("action") ?? "");

  if (
    !id ||
    (action !== "approve" && action !== "reject" && action !== "request_rerun")
  ) {
    throw new Error("Invalid review decision payload");
  }

  await postReviewDecision(id, action);
  redirect("/admin");
}
