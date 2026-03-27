import { getReviewDetail } from "../../../../lib/api";
import { submitReviewDecision } from "./actions";

type ReviewDetailPageProps = {
  params: Promise<{ id: string }>;
};

export default async function ReviewDetailPage({ params }: ReviewDetailPageProps) {
  const { id } = await params;
  const detail = await getReviewDetail(id);

  return (
    <section className="article-layout">
      <div className="article-layout__content">
        <p className="article-meta">Review Detail</p>
        <h1>{detail.headline}</h1>
        <p className="article-dek">{detail.dek}</p>

        <section>
          <h2>Decision Reasons</h2>
          <ul>
            {detail.reasons.map((reason) => (
              <li key={reason}>{reason}</li>
            ))}
          </ul>
        </section>

        <section>
          <h2>Narrative</h2>
          <p>{detail.draft.narrative}</p>
        </section>

        <section>
          <h2>Facts</h2>
          <ul>
            {detail.draft.facts.map((fact, index) => (
              <li key={`${detail.id}-fact-${index}`}>
                {fact.text ?? fact.content ?? "Fact pending"}
              </li>
            ))}
          </ul>
        </section>

        <section>
          <h2>Analysis</h2>
          <ul>
            {detail.draft.analysis.map((item, index) => (
              <li key={`${detail.id}-analysis-${index}`}>
                {item.text ?? item.content ?? "Analysis pending"}
              </li>
            ))}
          </ul>
        </section>

        <section>
          <h2>Sources</h2>
          <ul>
            {detail.draft.sources.map((source) => (
              <li key={`${detail.id}-${source.label}`}>
                <a href={source.url ?? "#"}>{source.title ?? source.label}</a>
                {(source.publisher || source.label !== source.title) && (
                  <p>
                    {source.publisher ?? source.label}
                    {source.url ? ` · ${source.url}` : ""}
                  </p>
                )}
              </li>
            ))}
          </ul>
        </section>

        <section>
          <h2>Editorial Flags</h2>
          <ul>
            {detail.draft.editorial_flags.length ? (
              detail.draft.editorial_flags.map((flag, index) => (
                <li key={`${detail.id}-flag-${index}`}>
                  {(flag.severity ?? "info").toUpperCase()}: {flag.message ?? "Flagged for review"}
                </li>
              ))
            ) : (
              <li>No editorial flags</li>
            )}
          </ul>
        </section>

        <section>
          <h2>Actions</h2>
          <div className="article-actions">
            <form action={submitReviewDecision}>
              <input type="hidden" name="id" value={detail.id} />
              <input type="hidden" name="action" value="approve" />
              <button type="submit">Approve</button>
            </form>
            <form action={submitReviewDecision}>
              <input type="hidden" name="id" value={detail.id} />
              <input type="hidden" name="action" value="reject" />
              <button type="submit">Reject</button>
            </form>
            <form action={submitReviewDecision}>
              <input type="hidden" name="id" value={detail.id} />
              <input type="hidden" name="action" value="request_rerun" />
              <button type="submit">Request Rerun</button>
            </form>
          </div>
        </section>
      </div>
    </section>
  );
}
