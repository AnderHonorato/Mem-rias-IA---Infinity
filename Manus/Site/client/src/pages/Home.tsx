/**
 * Arquivo Vivo: página editorial assimétrica que transforma memória, conversa
 * e conhecimento curado em uma trilha visual de decisões rastreáveis.
 */
import { useMemo, useState } from "react";
import {
  ArrowDownRight,
  ArrowUpRight,
  Check,
  ChevronRight,
  CircleDot,
  Copy,
  ExternalLink,
  Menu,
  ShieldCheck,
  Sparkles,
  X,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import {
  Accordion,
  AccordionContent,
  AccordionItem,
  AccordionTrigger,
} from "@/components/ui/accordion";

const ASSETS = {
  hero: "assets/memorias-hero-archive.png",
  layers: "assets/memorias-layered-system.png",
  conversation: "assets/memorias-conversation-network.png",
  trust: "assets/memorias-trust-detail.png",
  mark: "assets/memorias-brand-mark.png",
};

type LayerKey = "individual" | "conversa" | "curado";

const layers: Record<
  LayerKey,
  {
    label: string;
    eyebrow: string;
    title: string;
    text: string;
    path: string;
    trait: string;
    color: string;
  }
> = {
  individual: {
    label: "01 / Individual",
    eyebrow: "Memória de autoria",
    title: "Cada IA mantém seu próprio fio de contexto.",
    text: "Preferências, decisões e entregas permanecem organizadas por tema e mês. A autoria não se dilui quando a memória cresce.",
    path: "Manus/Memorias/",
    trait: "Rastreável por origem",
    color: "bg-[#0b7d75]",
  },
  conversa: {
    label: "02 / Conversa",
    eyebrow: "Coordenação append-only",
    title: "IAs trocam perguntas sem sobrescrever o histórico.",
    text: "Cada mensagem traz IA, data, fuso, destinatário, tipo, referência e ação esperada. A conversa fica legível até quando a equipe cresce.",
    path: "Conversa entre IAs/",
    trait: "Pergunta, resposta e handoff",
    color: "bg-[#c5664c]",
  },
  curado: {
    label: "03 / Curado",
    eyebrow: "Conhecimento compartilhado",
    title: "Só o que é explicável ganha contexto global.",
    text: "Fatos confirmados, decisões e fichas de projeto carregam origem, confiança, escopo e validade antes de orientar uma nova tarefa.",
    path: "Conhecimento Compartilhado/",
    trait: "Promovido com confiança",
    color: "bg-[#173a58]",
  },
};

const protocols = [
  {
    number: "01",
    title: "Identifique quem fala",
    text: "Nome da IA, horário e destinatário removem ambiguidade antes que ela vire retrabalho.",
  },
  {
    number: "02",
    title: "Diga em que se apoia",
    text: "Fato, hipótese, decisão e fonte seguem separados para que confiança seja verificável.",
  },
  {
    number: "03",
    title: "Registre o próximo movimento",
    text: "Toda conversa termina com uma ação esperada, um responsável ou a marcação NENHUMA.",
  },
];

const knowledgeRows = [
  ["Perfil de colaboração", "Preferências confirmadas", "ATIVO"],
  ["Mapa de projetos", "Objetivo, estado e próximo marco", "ATIVO"],
  ["Decisões", "Alternativas, motivo e reversão", "PRONTO"],
  ["Fontes e confiança", "Evidência antes de inferência", "ATIVO"],
  ["Perguntas em aberto", "Handoffs sem contexto perdido", "PRONTO"],
];

function scrollToSection(id: string) {
  document.getElementById(id)?.scrollIntoView({ behavior: "smooth", block: "start" });
}

export default function Home() {
  const [activeLayer, setActiveLayer] = useState<LayerKey>("individual");
  const [mobileNavOpen, setMobileNavOpen] = useState(false);
  const [copied, setCopied] = useState(false);
  const layer = useMemo(() => layers[activeLayer], [activeLayer]);

  const copyProtocol = async () => {
    const message =
      "## [AAAA-MM-DD HH:MM ±HHMM] NomeDaIA → Destinatário\n\n**Tipo:** PERGUNTA | RESPOSTA | ATUALIZAÇÃO | ALERTA | SOLICITAÇÃO\n\n**Em resposta a:** NOVA CONVERSA\n\n**Mensagem:** texto claro e autocontido.\n\n**Ação esperada:** NENHUMA\n\n**Confiança e fonte:** Alta; caminho ou link.";
    await navigator.clipboard?.writeText(message);
    setCopied(true);
    window.setTimeout(() => setCopied(false), 2200);
  };

  const navItems = [
    ["Arquitetura", "arquitetura"],
    ["Protocolo", "protocolo"],
    ["Conhecimento", "conhecimento"],
    ["Próximos passos", "proximos-passos"],
  ];

  return (
    <div className="min-h-screen overflow-x-hidden bg-[#f4f0e8] text-[#12263a]">
      <div className="route-noise" aria-hidden="true" />

      <header className="site-header">
        <button
          type="button"
          className="brand-lockup"
          onClick={() => scrollToSection("inicio")}
          aria-label="Ir para o início"
        >
          <img src={ASSETS.mark} alt="Símbolo Memórias IA" className="brand-mark" />
          <span>
            <strong>Memórias IA</strong>
            <small>INFINITY ARCHIVE</small>
          </span>
        </button>

        <nav className="desktop-nav" aria-label="Navegação principal">
          {navItems.map(([label, id]) => (
            <button key={id} type="button" onClick={() => scrollToSection(id)}>
              {label}
            </button>
          ))}
        </nav>

        <Button className="header-cta" onClick={() => scrollToSection("protocolo")}>
          Ver protocolo <ArrowDownRight size={16} />
        </Button>

        <Button
          variant="ghost"
          size="icon"
          className="mobile-menu"
          aria-label="Abrir navegação"
          onClick={() => setMobileNavOpen((isOpen) => !isOpen)}
        >
          {mobileNavOpen ? <X size={21} /> : <Menu size={21} />}
        </Button>
      </header>

      {mobileNavOpen && (
        <nav className="mobile-nav" aria-label="Navegação móvel">
          {navItems.map(([label, id]) => (
            <button
              key={id}
              type="button"
              onClick={() => {
                scrollToSection(id);
                setMobileNavOpen(false);
              }}
            >
              {label} <ChevronRight size={16} />
            </button>
          ))}
        </nav>
      )}

      <aside className="archive-spine" aria-label="Trilho de navegação do arquivo">
        <div className="spine-topmark">
          <img src={ASSETS.mark} alt="" />
          <span>IDX<br />∞.03</span>
        </div>
        <nav className="spine-nav" aria-label="Índice do arquivo">
          {[
            ["00", "Início", "inicio"],
            ["01", "Camadas", "arquitetura"],
            ["02", "Conversa", "protocolo"],
            ["03", "Curadoria", "conhecimento"],
            ["04", "Ação", "proximos-passos"],
          ].map(([number, label, id]) => (
            <button key={id} type="button" onClick={() => scrollToSection(id)}>
              <span className="spine-node" />
              <i>{number}</i>
              <b>{label}</b>
            </button>
          ))}
        </nav>
        <div className="spine-status">
          <span>SISTEMA</span>
          <b><i /> ATIVO</b>
          <small>REV. 2026.08</small>
        </div>
      </aside>

      <main>
        <section id="inicio" className="hero-section">
          <div className="hero-copy">
            <div className="eyebrow light-eyebrow">
              <span className="live-pip" /> ARQUITETURA DE COLABORAÇÃO
            </div>
            <h1>
              Contexto não é ruído. <em>É infraestrutura.</em>
            </h1>
            <p>
              Um sistema para coordenar múltiplas IAs sem perder autoria,
              confiança ou o fio que liga uma decisão à próxima.
            </p>
            <div className="hero-actions">
              <Button className="signal-button" onClick={() => scrollToSection("arquitetura")}>
                Explorar as camadas <ArrowDownRight size={17} />
              </Button>
              <button className="text-button" type="button" onClick={() => scrollToSection("conhecimento")}>
                Ver conhecimento curado <ArrowUpRight size={16} />
              </button>
            </div>
            <div className="hero-provenance">
              <span>ORIGEM <b>PROPOSTA / 2026.08</b></span>
              <span>ESTADO <b>EM OPERAÇÃO</b></span>
            </div>
            <div className="hero-statline">
              <span><b>3</b> camadas distintas</span>
              <span><b>1</b> contexto explicável</span>
            </div>
          </div>

          <div className="hero-visual">
            <img src={ASSETS.hero} alt="Arquivo físico abstrato conectado por trilhas verdes" />
            <div className="hero-image-frame" aria-hidden="true">
              <span>MEMÓRIA</span><i /> <span>CONVERSA</span><i /> <span>CONFIANÇA</span>
            </div>
          </div>

          <div className="hero-route" aria-hidden="true">
            <span>01</span><i /><span>02</span><i /><span>03</span>
          </div>
        </section>

        <section className="thesis-section">
          <div className="route-label"><CircleDot size={15} /> PRINCÍPIO DE PROJETO <span>CONFIANÇA / ALTA</span></div>
          <p>
            Coordenação, memória individual e conhecimento curado têm funções
            diferentes. Quando cada camada tem um lugar, a colaboração escala
            sem transformar conversa em verdade automática.
          </p>
          <div className="thesis-note">
            <ShieldCheck size={18} />
            <span>O usuário prevalece sobre memórias antigas e inferências de qualquer IA.</span>
          </div>
        </section>

        <section id="arquitetura" className="architecture-section">
          <div className="section-heading split-heading">
            <div>
              <div className="heading-meta"><span>CAMADA / SISTEMA</span><span>ORIGEM / ARQUIVO VIVO</span></div>
              <span className="eyebrow">01 / ARQUITETURA</span>
              <h2>Três lugares para não misturar o que tem pesos diferentes.</h2>
            </div>
            <p>
              A experiência começa com uma pergunta simples: este conteúdo é
              meu, é uma conversa ou já pode orientar todo mundo?
            </p>
          </div>

          <div className="architecture-grid">
            <div className="layer-rail" role="tablist" aria-label="Camadas do sistema">
              {(Object.keys(layers) as LayerKey[]).map((key, index) => (
                <button
                  key={key}
                  type="button"
                  role="tab"
                  aria-selected={activeLayer === key}
                  className={activeLayer === key ? "layer-tab active" : "layer-tab"}
                  onClick={() => setActiveLayer(key)}
                >
                  <span>0{index + 1}</span>
                  <b>{layers[key].eyebrow}</b>
                  <ChevronRight size={18} />
                </button>
              ))}
            </div>

            <article className="layer-detail" role="tabpanel">
              <div className="panel-meta"><span>ORIGEM / ROTEADOR</span><span>ESTADO / INDEXADO</span></div>
              <div className={`status-dot ${layer.color}`} />
              <span className="card-kicker">{layer.label}</span>
              <h3>{layer.title}</h3>
              <p>{layer.text}</p>
              <div className="path-chip"><span>PATH</span>{layer.path}</div>
              <div className="trait-line"><Check size={15} /> {layer.trait}</div>
            </article>

            <div className="layers-image-wrap">
              <img src={ASSETS.layers} alt="Três camadas físicas de um sistema de conhecimento" />
              <div className="image-caption">camadas que não se confundem</div>
            </div>
          </div>
        </section>

        <section id="protocolo" className="protocol-section">
          <div className="protocol-intro">
            <div className="eyebrow light-eyebrow">02 / CONVERSA ENTRE IAS</div>
            <div className="protocol-status"><span>RESPONSÁVEL / TODAS AS IAS</span><b><i /> ESTADO / ABERTO</b></div>
            <h2>Conversem no mesmo mural. <em>Não falem por cima.</em></h2>
            <p>
              O arquivo compartilhado vira um handoff legível: quem escreveu,
              para quem, em resposta a quê e qual movimento vem agora.
            </p>
            <Button className="outline-signal" onClick={copyProtocol}>
              {copied ? <Check size={16} /> : <Copy size={16} />}
              {copied ? "Modelo copiado" : "Copiar modelo de mensagem"}
            </Button>
          </div>
          <div className="protocol-visual">
            <img src={ASSETS.conversation} alt="Fichas abstratas conectadas em torno de um registro compartilhado" />
            <div className="message-sample">
              <div className="sample-header"><span>ORIGEM / CONVERSA ENTRE IAS</span><span>CONFIANÇA / ALTA</span></div>
              <div><span className="message-dot" /> <b>Manus</b> <i>→ GPT</i></div>
              <p>Qual decisão ainda precisa de confirmação?</p>
              <small>PERGUNTA · 22:34 −03</small>
            </div>
          </div>
        </section>

        <section className="protocol-steps">
          {protocols.map((item) => (
            <article key={item.number}>
              <span>{item.number}</span>
              <h3>{item.title}</h3>
              <p>{item.text}</p>
            </article>
          ))}
        </section>

        <section id="conhecimento" className="knowledge-section">
          <div className="knowledge-image">
            <img src={ASSETS.trust} alt="Materiais de arquivo que representam confiança e revisão" />
            <div className="image-index">CONF. / 0.98</div>
          </div>
          <div className="knowledge-copy">
            <div className="heading-meta"><span>CAMADA / CURADA</span><span>ESTADO / REVISÁVEL</span></div>
            <span className="eyebrow">03 / CONHECIMENTO CURADO</span>
            <h2>Promova apenas o que pode ser explicado, localizado e revisado.</h2>
            <p>
              Contexto global não é uma cópia de tudo. É uma seleção com origem,
              confiança, escopo e validade, pronta para orientar a próxima IA.
            </p>
            <a
              className="repository-link"
              href="https://github.com/AnderHonorato/Mem-rias-IA---Infinity"
              target="_blank"
              rel="noreferrer"
            >
              Ver estrutura no repositório <ExternalLink size={16} />
            </a>
          </div>
          <div className="knowledge-ledger">
            <div className="ledger-header"><span>CONHECIMENTO COMPARTILHADO</span><b>ÍNDICE / ESTADO</b></div>
            {knowledgeRows.map(([name, detail, state]) => (
              <div className="ledger-row" key={name}>
                <div><b>{name}</b><span>{detail}</span></div>
                <em>{state}</em>
              </div>
            ))}
          </div>
        </section>

        <section className="trust-section">
          <div className="trust-copy">
            <div className="heading-meta"><span>ORIGEM / PROTOCOLO</span><span>CAMADA / CONFIANÇA</span></div>
            <span className="eyebrow">GUARDA-CHUVA DE CONFIANÇA</span>
            <h2>Conhecimento sem origem é só uma hipótese bem formatada.</h2>
          </div>
          <div className="trust-grid">
            <div><span>FATO</span><p>Confirmado pelo usuário ou fonte verificável.</p></div>
            <div><span>HIPÓTESE</span><p>Útil para investigar, mas nunca promovida sozinha.</p></div>
            <div><span>DECISÃO</span><p>Inclui alternativas, motivo, impacto e revisão.</p></div>
          </div>
        </section>

        <section id="proximos-passos" className="next-section">
          <div className="next-heading">
            <div className="heading-meta"><span>RESPONSÁVEL / USUÁRIO + IAS</span><span>ESTADO / PRÓXIMO</span></div>
            <span className="eyebrow">PRÓXIMOS PASSOS</span>
            <h2>Faça a memória trabalhar a favor do próximo projeto.</h2>
          </div>
          <div className="next-list">
            <div><span>01</span><p>Preencha o perfil de colaboração só com preferências confirmadas.</p><ArrowUpRight size={19} /></div>
            <div><span>02</span><p>Crie uma ficha por projeto com escopo, stack, risco e próximo marco.</p><ArrowUpRight size={19} /></div>
            <div><span>03</span><p>Conecte decisões, fontes e perguntas em aberto ao mural de conversas.</p><ArrowUpRight size={19} /></div>
          </div>
        </section>

        <section className="faq-section">
          <div>
            <div className="heading-meta"><span>ORIGEM / ÍNDICE</span><span>ESTADO / CONSULTÁVEL</span></div>
            <span className="eyebrow">EM UMA FRASE</span>
            <h2>Memória útil é aquela que sabe de onde veio e para onde vai.</h2>
          </div>
          <Accordion type="single" collapsible className="faq-accordion">
            <AccordionItem value="item-1">
              <AccordionTrigger>O que deve entrar no conhecimento compartilhado?</AccordionTrigger>
              <AccordionContent>
                Fatos confirmados, decisões globais, contexto de projeto e fontes que ajudem mais de uma IA — sempre com origem, data, confiança, escopo e validade.
              </AccordionContent>
            </AccordionItem>
            <AccordionItem value="item-2">
              <AccordionTrigger>O que continua sendo memória individual?</AccordionTrigger>
              <AccordionContent>
                Rascunhos, preferências locais, registros operacionais e contexto de autoria permanecem na pasta da IA responsável, organizados por tema e mês.
              </AccordionContent>
            </AccordionItem>
            <AccordionItem value="item-3">
              <AccordionTrigger>Como proteger informações sensíveis?</AccordionTrigger>
              <AccordionContent>
                A regra é minimização: nunca guardar senhas, tokens, cookies, chaves privadas, códigos de recuperação ou dados pessoais desnecessários para a próxima tarefa.
              </AccordionContent>
            </AccordionItem>
          </Accordion>
        </section>
      </main>

      <footer className="site-footer">
        <div className="footer-brand"><img src={ASSETS.mark} alt="" /><span>Memórias IA <i>∞</i></span></div>
        <p>Um arquivo vivo para contexto, autoria e colaboração entre IAs.</p>
        <button type="button" onClick={() => scrollToSection("inicio")}>Voltar ao topo <ArrowUpRight size={15} /></button>
      </footer>

      <div className="floating-route" aria-hidden="true"><Sparkles size={14} /> CONTEXTO ATIVO</div>
    </div>
  );
}
