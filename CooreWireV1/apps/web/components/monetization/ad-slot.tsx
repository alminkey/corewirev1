type AdSlotProps = {
  placement: "homepage-feed" | "homepage-lower" | "article-upper" | "article-lower";
};

const GOOGLE_ADSENSE_CLIENT_ID = process.env.GOOGLE_ADSENSE_CLIENT_ID ?? "";
const COREWIRE_ADSENSE_ENABLED = process.env.COREWIRE_ADSENSE_ENABLED ?? "false";

export function AdSlot({ placement }: AdSlotProps) {
  if (COREWIRE_ADSENSE_ENABLED !== "true") {
    return (
      <aside className="cw-panel cw-ad-slot" data-placement={placement}>
        <div className="cw-panel-header">
          <span>Ad Slot</span>
          <span>{placement}</span>
        </div>
        <div className="cw-article-section">
          <p>Reserved monetization slot.</p>
        </div>
      </aside>
    );
  }

  return (
    <aside className="cw-panel cw-ad-slot" data-placement={placement}>
      <ins
        className="adsbygoogle"
        data-ad-client={GOOGLE_ADSENSE_CLIENT_ID}
        data-ad-slot={placement}
        data-ad-format="auto"
        data-full-width-responsive="true"
      />
    </aside>
  );
}
