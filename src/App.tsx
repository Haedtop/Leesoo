import {useEffect, useMemo, useState, type ReactNode} from 'react';
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
    {href: '#overview', label: '소개'},
    {href: '#projects', label: '프로젝트'},
    {href: '#strengths', label: '기획 방식'},
    {href: '#contact', label: '연락처'},
  ];

  return (
    <header className="site-header">
      <button className="brand-button" onClick={navigateHome} type="button">
        <span className="brand-mark">LJ</span>
        <span>
          <strong>이정수</strong>
          <small>MMORPG System / Balance Planner</small>
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
  children?: ReactNode;
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
    <article
      aria-label={`${project.title} 상세 보기`}
      className="project-card"
      onClick={() => navigateProject(project.id)}
      onKeyDown={(event) => {
        if (event.key === 'Enter' || event.key === ' ') {
          event.preventDefault();
          navigateProject(project.id);
        }
      }}
      role="button"
      tabIndex={0}
    >
      <div className="project-card-top">
        <div className="project-icon">
          <Icon size={22} />
        </div>
        <div>
          <span className="project-category">
            {project.category} / {project.caseType}
          </span>
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
      <span className="text-button" aria-hidden="true">
        상세 보기
        <ArrowRight size={16} />
      </span>
    </article>
  );
}

function HomePage() {
  const highlightedProjects = projects.slice(0, 3);

  return (
    <main>
      <section className="hero" id="overview">
        <div className="hero-copy">
          <p className="eyebrow">MMORPG System / Balance Planner</p>
          <h1>성장, 보상, 전투 구조를 운영 가능한 규칙으로 정리하는 기획자</h1>
          <p className="hero-summary">
            라이온하트 스튜디오에서 2023.11부터 2026.06.21까지
            <br />
            오딘: 발할라 라이징의 시스템/밸런스 기획 업무를 수행했습니다.
            콘텐츠 추가보다 유저의 반복 동기, 재화 흐름, 성장 체감, 운영 리스크가
            맞물리는 구조를 중요하게 봅니다.
          </p>
          <div className="hero-actions">
            <a className="primary-action" href="#projects">
              주요 프로젝트
              <ArrowRight size={17} />
            </a>
            <a className="secondary-action" href={portfolioPdfUrl}>
              <Download size={17} />
              PDF 요약본
            </a>
          </div>
        </div>

        <div className="hero-panel" aria-label="업무 범위 요약">
          <div className="panel-header">
            <span>Work Scope</span>
            <strong>Live MMORPG</strong>
          </div>
          <div className="signal-grid">
            <MetricCard label="대표 업무" value="6개" note="실제 업무 문서 기반" />
            <MetricCard label="정리 구조" value="6단계" note="소개/배경/분석/역할/결과/효과" />
            <MetricCard label="성과 표기" value="분리" note="실제 결과와 기대 효과 구분" />
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
          <strong>직무</strong>
          <span>MMORPG 시스템/밸런스 기획</span>
        </div>
        <div>
          <strong>검토 축</strong>
          <span>성장 체감, 보상 기대값, 전투 시간, 재화 흐름, 운영 리스크</span>
        </div>
        <div>
          <strong>문서 기준</strong>
          <span>실제 결과는 확인된 범위만 쓰고, 제안 단계는 기대 효과로 분리</span>
        </div>
      </section>

      <section className="content-section" id="projects">
        <SectionLabel eyebrow="Projects" title="주요 프로젝트">
          <p>
            각 프로젝트는 시스템 소개, 업무 배경, 검토 기준, 내 역할, 실제 결과,
            기대 효과를 분리해 정리했습니다. 내부 수치는 공개 가능한 범위로 재가공했습니다.
          </p>
        </SectionLabel>
        <div className="project-grid">
          {projects.map((project) => (
            <ProjectCard key={project.id} project={project} />
          ))}
        </div>
      </section>

      <section className="content-section compact" id="strengths">
        <SectionLabel eyebrow="Work Style" title="기획 방식">
          <p>
            기능을 먼저 늘리기보다 목적, 유저 판단, 보상 구조, 재화 흐름, 예외 케이스를
            먼저 정리합니다.
          </p>
        </SectionLabel>
        <div className="strength-grid">
          <div className="strength-item">
            <Target size={24} />
            <h3>목적과 제약 분리</h3>
            <p>
              상위 방향을 그대로 기능 목록으로 옮기지 않고, 해결해야 할 문제와 건드리면 안 되는
              제약을 먼저 나눕니다.
            </p>
          </div>
          <div className="strength-item">
            <BarChart3 size={24} />
            <h3>수치와 체감 연결</h3>
            <p>
              포인트, HP, TTK, 보상 공급량 같은 수치를 유저 진행 속도와 반복 동기 기준으로
              해석합니다.
            </p>
          </div>
          <div className="strength-item">
            <ShieldCheck size={24} />
            <h3>운영 리스크 점검</h3>
            <p>
              상위 유저 독점, 신규/복귀 유저 진입 장벽, 거래소 영향, 재화 인플레이션 가능성을
              함께 확인합니다.
            </p>
          </div>
        </div>
      </section>

      <section className="content-section compact">
        <SectionLabel eyebrow="Document Frame" title="프로젝트 문서 구조" />
        <div className="flow-row">
          {['소개', '배경', '분석', '역할', '결과'].map((item, index) => (
            <div className="flow-step" key={item}>
              <span>{String(index + 1).padStart(2, '0')}</span>
              <strong>{item}</strong>
            </div>
          ))}
        </div>
      </section>

      <section className="content-section compact">
        <SectionLabel eyebrow="Featured" title="먼저 읽기 좋은 사례" />
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
            <p className="eyebrow">
              {project.category} / {project.caseType}
            </p>
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
        <DetailSection title="업무 배경" items={project.problem} />
        <DetailSection title="분석 기준" items={project.analysis} />
        <DetailSection title="내 역할" items={project.role} />
        <DetailSection title="설계/검토 방향" items={project.design} />
        <DetailSection title="실제 결과" items={project.actualResult} variant="result" />
        <DetailSection title="기대 효과" items={project.expectedEffect} variant="result" />
      </section>

      <section className="next-project">
        <div>
          <span>다음 프로젝트</span>
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
