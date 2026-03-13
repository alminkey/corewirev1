import { AdminShell } from "../../components/admin/admin-shell";
import { AutonomyControls } from "../../components/admin/autonomy-controls";


export default function AdminPage() {
  return (
    <>
      <AdminShell
        publishMode="Hybrid"
        systemHealth="Stable"
        reviewQueueCount={3}
      />
      <AutonomyControls
        mode="hybrid"
        homepageAutoPublish={true}
        developingStoryAutoPublish={true}
        pauseIngest={false}
        pausePublish={false}
      />
    </>
  );
}
