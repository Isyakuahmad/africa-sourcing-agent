* { box-sizing: border-box; }
body {
  margin: 0;
  font-family: Arial, sans-serif;
  background: #f4f7fb;
  color: #1e293b;
}
.container {
  width: min(1100px, calc(100% - 2rem));
  margin: 0 auto;
}
.topbar {
  background: #0f172a;
  color: white;
  padding: 1rem 0;
}
.nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.brand a, nav a {
  color: white;
  text-decoration: none;
}
nav {
  display: flex;
  gap: 1rem;
}
.main-content {
  padding: 2rem 0 3rem;
}
.stats-grid, .section-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 1rem;
}
.card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 10px 30px rgba(15, 23, 42, 0.06);
  padding: 1.2rem;
  margin-bottom: 1.5rem;
}
.stat strong {
  display: block;
  font-size: 2rem;
  margin-top: 0.25rem;
}
.label {
  color: #475569;
  font-size: 0.8rem;
  text-transform: uppercase;
}
.list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: grid;
  gap: 0.75rem;
}
.list li {
  display: flex;
  justify-content: space-between;
  gap: 1rem;
  border-bottom: 1px solid #e2e8f0;
  padding-bottom: 0.5rem;
}
.form-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 1rem;
}
label {
  display: flex;
  flex-direction: column;
  gap: 0.35rem;
  font-weight: 600;
}
input, select, textarea, button {
  font: inherit;
}
input, select, textarea {
  border: 1px solid #cbd5e1;
  border-radius: 9px;
  padding: 0.7rem 0.8rem;
}
button, .button {
  border: none;
  border-radius: 10px;
  padding: 0.7rem 1rem;
  text-decoration: none;
  display: inline-block;
  cursor: pointer;
}
.primary {
  background: #2563eb;
  color: white;
}
.secondary {
  background: #e2e8f0;
  color: #0f172a;
}
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1rem;
}
.detail-list {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 1rem;
}
.detail-list div {
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  padding: 0.75rem;
}
.detail-list dt {
  color: #475569;
  font-size: 0.82rem;
  text-transform: uppercase;
}
.detail-list dd {
  margin: 0.3rem 0 0;
  font-weight: 600;
}
.candidate-box {
  border: 1px solid #dbeafe;
  background: #f8fbff;
  border-radius: 12px;
  padding: 1rem;
  margin-bottom: 1rem;
}
.candidate-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
}
.badge {
  display: inline-block;
  padding: 0.35rem 0.7rem;
  border-radius: 999px;
  font-size: 0.8rem;
  font-weight: 700;
}
.badge.success { background: #dcfce7; color: #166534; }
.badge.warn { background: #fef3c7; color: #92400e; }
.full-width {
  grid-column: 1 / -1;
}
.alert.demo {
  background: #fff7ed;
  border: 1px solid #fdba74;
  color: #9a5b00;
  border-radius: 10px;
  padding: 0.75rem 1rem;
  margin-bottom: 1rem;
}
pre {
  white-space: pre-wrap;
  word-break: break-word;
}
@media (max-width: 700px) {
  .nav, .page-header {
    flex-direction: column;
    align-items: flex-start;
  }
}
