import { NavLink, Outlet } from "react-router-dom";

export function Layout() {
  return (
    <div className="app-shell">
      <header className="nav">
        <NavLink to="/" className="nav-brand" end>
          Startup Valuation &amp; Analysis
        </NavLink>
        <nav className="nav-links">
          <NavLink
            to="/"
            end
            className={({ isActive }) => (isActive ? "active" : "")}
          >
            Home
          </NavLink>
          <NavLink
            to="/public"
            className={({ isActive }) => (isActive ? "active" : "")}
          >
            Public Company
          </NavLink>
          <NavLink
            to="/startup"
            className={({ isActive }) => (isActive ? "active" : "")}
          >
            Startup Valuation
          </NavLink>
        </nav>
      </header>
      <main className="page">
        <Outlet />
      </main>
    </div>
  );
}
