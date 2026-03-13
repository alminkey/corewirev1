import { AdminShell } from "../../components/admin/admin-shell";


export default function AdminPage() {
  return (
    <AdminShell
      publishMode="Hybrid"
      systemHealth="Stable"
      reviewQueueCount={3}
    />
  );
}
