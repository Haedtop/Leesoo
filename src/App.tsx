import {useEffect, useMemo, useState} from 'react';
import {
  ArrowLeft,
  ArrowRight,
  BarChart3,
  Download,
  Mail,
  Menu,
  Phone,
  ShieldCheck,
  Target,
  X,
} from 'lucide-react';
import {ProjectCase, projects} from './data/projects';

const portfolioPdfUrl = `${import.meta.env.BASE_URL}portfolio-summary.pdf`;

type RouteState = {
  page: 'home' | 'project';
  projectId?: string;
};

const parseRoute = (): RouteState => {
  const hash = window.location.hash.replace(/^#\/?/, '');
  const [, projectId] = hash.match(/^projects\/(.+)$/) ?? [];

  if (projectId && projects.some((project) => project.id === projectId)) {
    return {page: 'project', projectId};
  }

  return {page: 'home'};
};

const navigateHome = () => {
  window.location.hash = '';
  window.scrollTo({top: 0, behavior: 'smooth'});
};

const navigateProject = (projectId: string) => {
  window.location.hash = `/projects/${projectId}`;
  window.scrollTo({top: 0, behavior: 'smooth'});
};

function useHashRoute() {
  const [route, setRoute] = useState<RouteState>(() => parseRoute());

  useEffect(() => {
    const handleHashChange = () => setRoute(parseRoute());
    window.addEventListener('hashchange', handleHashChange);
    return () => window.removeEventListener('hashchange', handleHashChange);
  }, []);

  return route;
}

function Nav() {
  const [isOpen, setIsOpen] = useState(false);
  const links = [
    {href: '#overview', label: '개요'},
    {href: '#projects', label: '프로젝트'},
    {href: '#strengths', label: '역량'},
    {href: '#contact', label: '연락처'},
  ];

  return (
    <header className="site-header">
      <button className="brand-button" onClick={navigateHome} type="button">
        <span className="brand-mark">LJ</span>
        <span>
          <strong>이정수</strong>
          <small>MMORPG System Designer</small>
        </span>
      </button>

      <nav className="desktop-nav" aria-label="주요 메뉴">
        {links.map((link) => (
          <a key={link.href} href={link.href}>
            {link.label}
          </a>
        ))}
      </nav>

      <a className="desktop-cta" href={portfolioPdfUrl}>
        <Download size={16} />
        PDF
      </a>

      <button
        className="menu-button"
        type="button"
        aria-label="모바일 메뉴 열기"
        onClick={() => setIsOpen(true)}
      >
        <Menu size={22} />
      </button>

      {isOpen && (
        <div className="mobile-nav" role="dialog" aria-modal="true">
          <button
            className="mobile-close"
            type="button"
            aria-label="모바일 메뉴 닫기"
            onClick={() => setIsOpen(false)}
          >
            <X size={22} />
          </button>
          {links.map((link) => (
            <a key={link.href} href={link.href} onClick={() => setIsOpen(false)}>
              {link.label}
            </a>
          ))}
          <a href={portfolioPdfUrl} onClick={() => setIsOpen(false)}>
            PDF 요약본
          </a>
        </div>
      )}
    </header>
  );
}

function MetricCard({
  label,
  value,
  note,
}: {
  label: string;
  value: string;
  note: string;
}) {
  return (
    <div className="metric-card">
      <span>{label}</span>
      <strong>{value}</strong>
      <small>{note}</small>
    </div>
  );
}

function SectionLabel({
  eyebrow,
  title,
  children,
}: {
  eyebrow: string;
  title: string;
  children?: React.ReactNode;
}) {
  return (
    <div className="section-label">
      <p>{eyebrow}</p>
      <h2>{title}</h2>
      {children && <div className="section-copy">{children}</div>}
    </div>
  );
}

function ProjectCard({project}: {project: ProjectCase}) {
  const Icon = project.icon;

  return (
    <article className="project-card">
      <div className="project-card-top">
        <div className="project-icon">
          <Icon size={22} />
        </div>
        <div>
          <span className="project-category">{project.category}</span>
          <h3>{project.shortTitle}</h3>
        </div>
      </div>
      <p>{project.summary}</p>
      <div className="project-card-metrics">
        {project.sanitizedMetrics.slice(0, 2).map((metric) => (
          <span key={metric.label}>
            <b>{metric.label}</b>
            {metric.value}
          </span>
        ))}
      </div>
      <button
        className="text-button"
        type="button"
        onClick={() => navigateProject(project.id)}
      >
        상세 보기
        <ArrowRight size={16} />
      </button>
    </article>
  );
}

function HomePage() {
  const highlightedProjects = projects.slice(0, 3);

  return (
    <main>
      <section className="hero" id="overview">
        <div className="hero-copy">
          <p className="eyebrow">MMORPG 시스템/밸런스 기획자</p>
          <h1>문제를 수치로 확인하고, 구조로 해결하는 기획자 이정수</h1>
          <p className="hero-summary">
            전투, 성장, 보상, 경제 흐름을 분리해서 보지 않고 하나의 플레이
            구조로 연결해 설계합니다.
          </p>
          <div className="hero-actions">
            <a className="primary-action" href="#projects">
              대표 프로젝트
              <ArrowRight size={17} />
            </a>
            <a className="secondary-action" href={portfolioPdfUrl}>
              <Download size={17} />
              PDF 요약본
            </a>
          </div>
        </div>

        <div className="hero-panel" aria-label="핵심 역량 요약">
          <div className="panel-header">
            <span>Core Signal</span>
            <strong>System Balance</strong>
          </div>
          <div className="signal-grid">
            <MetricCard
              label="대표 사례"
              value="6개"
              note="검증 가능한 원문 기반"
            />
            <MetricCard
              label="문서 구조"
              value="5단계"
              note="문제/분석/역할/설계/결과"
            />
            <MetricCard
              label="성과 표기"
              value="분리"
              note="실제 결과와 기대 효과 구분"
            />
          </div>
          <div className="system-map" aria-hidden="true">
            <span>전투</span>
            <span>성장</span>
            <span>보상</span>
            <span>경제</span>
          </div>
        </div>
      </section>

      <section className="summary-band">
        <div>
          <strong>포지션</strong>
          <span>MMORPG 시스템/밸런스</span>
        </div>
        <div>
          <strong>핵심 강점</strong>
          <span>지표 분석, 보상 기대값, 성장 곡선, 경제 리스크 제어</span>
        </div>
        <div>
          <strong>작성 기준</strong>
          <span>과장 제거, 수치 범위화, 실제 결과/기대 효과 분리</span>
        </div>
      </section>

      <section className="content-section" id="projects">
        <SectionLabel eyebrow="Case Studies" title="대표 프로젝트">
          <p>
            기존 웹 포트폴리오 4개 사례에 길드 연구/의뢰와 PvP TTK 개선안을
            추가했습니다. 모든 사례는 같은 목차로 읽히도록 정리했습니다.
          </p>
        </SectionLabel>
        <div className="project-grid">
          {projects.map((project) => (
            <ProjectCard key={project.id} project={project} />
          ))}
        </div>
      </section>

      <section className="content-section compact" id="strengths">
        <SectionLabel eyebrow="Strengths" title="면접관이 바로 읽어야 할 강점">
          <p>
            장황한 감성 문구보다 실무 판단 근거가 보이도록 강점을 짧게
            고정했습니다.
          </p>
        </SectionLabel>
        <div className="strength-grid">
          <div className="strength-item">
            <Target size={24} />
            <h3>목적 우선 설계</h3>
            <p>
              기능을 먼저 늘리지 않고 어떤 문제를 해결할지, 어떤 유저 판단을
              만들지 먼저 정의합니다.
            </p>
          </div>
          <div className="strength-item">
            <BarChart3 size={24} />
            <h3>수치 기반 검증</h3>
            <p>
              TTK, 보상 기대값, 포인트 허들, 공급량을 함께 보며 구조가 실제로
              작동할지 확인합니다.
            </p>
          </div>
          <div className="strength-item">
            <ShieldCheck size={24} />
            <h3>리스크 제어</h3>
            <p>
              상위 유저 독점, 신규/복귀 유저 진입 장벽, 인플레이션, BM 가치
              훼손을 함께 검토합니다.
            </p>
          </div>
        </div>
      </section>

      <section className="content-section compact">
        <SectionLabel eyebrow="Interview View" title="프로젝트별 읽기 흐름" />
        <div className="flow-row">
          {['문제', '분석', '내 역할', '설계', '결과'].map((item, index) => (
            <div className="flow-step" key={item}>
              <span>{String(index + 1).padStart(2, '0')}</span>
              <strong>{item}</strong>
            </div>
          ))}
        </div>
      </section>

      <section className="content-section compact">
        <SectionLabel eyebrow="Featured" title="빠르게 볼 대표 사례 3개" />
        <div className="featured-list">
          {highlightedProjects.map((project) => (
            <button
              className="featured-row"
              key={project.id}
              type="button"
              onClick={() => navigateProject(project.id)}
            >
              <span>{project.category}</span>
              <strong>{project.title}</strong>
              <ArrowRight size={17} />
            </button>
          ))}
        </div>
      </section>
    </main>
  );
}

function DetailSection({
  title,
  items,
  variant = 'default',
}: {
  title: string;
  items: string[];
  variant?: 'default' | 'result';
}) {
  return (
    <section className={`detail-block ${variant}`}>
      <h2>{title}</h2>
      <ul>
        {items.map((item) => (
          <li key={item}>{item}</li>
        ))}
      </ul>
    </section>
  );
}

function ProjectPage({project}: {project: ProjectCase}) {
  const Icon = project.icon;
  const nextProject = useMemo(() => {
    const index = projects.findIndex((item) => item.id === project.id);
    return projects[(index + 1) % projects.length];
  }, [project.id]);

  return (
    <main className="project-page">
      <section className="project-hero">
        <button className="back-button" type="button" onClick={navigateHome}>
          <ArrowLeft size={17} />
          목록으로
        </button>
        <div className="project-hero-grid">
          <div>
            <p className="eyebrow">{project.category}</p>
            <h1>{project.title}</h1>
            <p>{project.summary}</p>
          </div>
          <div className="project-fact-panel">
            <Icon size={34} />
            <span>기간</span>
            <strong>{project.period}</strong>
            <small>{project.sourceNote}</small>
          </div>
        </div>
      </section>

      <section className="metric-strip">
        {project.sanitizedMetrics.map((metric) => (
          <MetricCard
            key={metric.label}
            label={metric.label}
            value={metric.value}
            note={metric.note}
          />
        ))}
      </section>

      <section className="detail-grid">
        <DetailSection title="문제" items={project.problem} />
        <DetailSection title="분석" items={project.analysis} />
        <DetailSection title="내 역할" items={project.role} />
        <DetailSection title="설계" items={project.design} />
        <DetailSection
          title="실제 결과"
          items={project.actualResult}
          variant="result"
        />
        <DetailSection
          title="기대 효과"
          items={project.expectedEffect}
          variant="result"
        />
      </section>

      <section className="next-project">
        <div>
          <span>다음 사례</span>
          <strong>{nextProject.title}</strong>
        </div>
        <button type="button" onClick={() => navigateProject(nextProject.id)}>
          보기
          <ArrowRight size={17} />
        </button>
      </section>
    </main>
  );
}

function Footer() {
  return (
    <footer className="site-footer" id="contact">
      <div>
        <p className="eyebrow">Contact</p>
        <h2>이정수</h2>
        <p>MMORPG 시스템/밸런스 기획자</p>
      </div>
      <div className="footer-links">
        <a href="mailto:jjangsoo8571@gmail.com">
          <Mail size={17} />
          jjangsoo8571@gmail.com
        </a>
        <a href="tel:01080488571">
          <Phone size={17} />
          010-8048-8571
        </a>
        <a href={portfolioPdfUrl}>
          <Download size={17} />
          PDF 요약본
        </a>
      </div>
    </footer>
  );
}

export default function App() {
  const route = useHashRoute();
  const project =
    route.page === 'project'
      ? projects.find((item) => item.id === route.projectId)
      : undefined;

  return (
    <div className="app-shell">
      <Nav />
      {project ? <ProjectPage project={project} /> : <HomePage />}
      <Footer />
    </div>
  );
}
