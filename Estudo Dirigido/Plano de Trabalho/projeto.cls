%%%%%%%%%%%%%%%% AVISO!
%% Altere as configurações do seu projeto no aquivo conf.tex
%% Evite fazer alterações nesse arquivo
%%%%%%%%%%%%%%%% CRÉDITOS
%% Baseado no projeto de Lauro César Araujo e equipe anbTeX
%% https://www.abntex.net.br/
%% Baseado no projeto de Adriano J. Holanda, DCM/FFCLRP/USP
%% https://gitlab.uspdigital.usp.br/sidcm/modelos-ppgca
%% ==========================================================================
%%
%% Copyright (c) 2020 Gabriel Morete de Azevedo
%%
%% This software is distributed under MIT License
%% https://opensource.org/licenses/MIT
%% ==========================================================================
%% https://github.com/gabrielmorete/Modelo-de-Projeto

\NeedsTeXFormat{LaTeX2e}
\ProvidesClass{projeto}

%%%%%%%%%%%%%%%% ESTRUTURA DA CLASSE 
% Declaração de opções
% Extensão da classe abntex2

\def\@@ptsize{12pt}
\DeclareOption{10pt}{\def\@@ptsize{10pt}}
\DeclareOption{11pt}{\def\@@ptsize{11pt}}
\DeclareOption{12pt}{\def\@@ptsize{12pt}}
\DeclareOption*{\PassOptionsToClass{\CurrentOption}{abnt2}}
\ProcessOptions\relax
\LoadClass[article,a4paper,\@@ptsize]{abntex2}

%%%%%%%%%%%%%%%% LaTeX
\RequirePackage{iftex} % Checa qual compilador está em uso
\ifXeTeX % XeTeX
    \RequirePackage{fontspec}
    \RequirePackage{polyglossia}
    \setdefaultlanguage{brazil}
    \defaultfontfeatures{Ligatures={TeX}}
\else % LaTeX, pdfLaTeX
    \RequirePackage[utf8]{inputenc}
    \RequirePackage[brazil]{babel}
    \RequirePackage[T1]{fontenc}
\fi

\ifLuaTeX % LuaTeX
    \RequirePackage{fontspec}
    \RequirePackage{polyglossia}
    \setdefaultlanguage{brazil}
    \defaultfontfeatures{Ligatures={TeX}}
\fi

%%%%%%%%%%%%%%%% PACOTES
\RequirePackage{etoolbox} % Ferramentas uteis
\RequirePackage{lmodern} % Usa a fonte Latin Modern
\RequirePackage{indentfirst} % Indenta o primeiro parágrafo de cada seção.
\RequirePackage{setspace} % Espaçamento
\RequirePackage{nomencl} % Lista de símbolos
\RequirePackage{graphicx} % Inclusão de gráficos
\RequirePackage{multirow} % Tabelas
\RequirePackage{multicol} % Formatação
\RequirePackage{mathtools} % Matemática, evolução do amsmath
\RequirePackage{amsthm} % Digitar teoremas e afins
\RequirePackage{amssymb} % Símbolos de matemática
\RequirePackage{hyperref}


%%%%%%%%%%%%%%%% Margens
%% Padrão abnTeX
\OnehalfSpacing % Outros : \SingleSpacing,\DoubleSpacing
\setlrmarginsandblock{3cm}{2cm}{*}
\setulmarginsandblock{3cm}{2cm}{*}
\checkandfixthelayout
%% Configuração será ignorada ao importar pacote fullpage

%%%%%%%%%%%%%%%% SEÇÕES
\RequirePackage{titlesec} 
\titleformat{\section}[hang]{\normalfont\Large\bfseries}{\thesection}{1em}{}
\titleformat{\subsection}[hang]{\normalfont\large\bfseries}{\thesubsection}{1em}{}

  
%%%%%%%%%%%%%%%% BIBLIOGRAFIA 
\newcommand\mybibname{Refer\^{e}ncias}

\renewcommand\bibsection{%
    \section*{\mybibname}
}
% Salva se abnt está em usa para não gerar conflito de estilo
\newcounter{__usandoabnt}
\setcounter{__usandoabnt}{0}

\AtBeginDocument{ 
    \@ifpackageloaded{backref}{ % Controle do backref
        \renewcommand{\backrefpagesname}{Citado na(s) página(s):~}
        % Texto padrão antes do número das páginas
        \renewcommand{\backref}{}
        % Define os textos da citação
        \renewcommand*{\backrefalt}[4]{
    	\ifcase #1 %
    		(Nenhuma citação no texto)%
    	\or
    		(Citado na página #2)%
    	\else
    		(Citado #1 vezes nas páginas #2)%
    	\fi}%
    }{}
    
    \@ifpackageloaded{abntex2cite}{ % Controle da bibliografia
        \setcounter{__usandoabnt}{1}
    }{}
}

% Tradução do comando
\newcommand{\bibliografia}[1]{
    \bibliography{#1}
}

% Comando para automatizar a troca de bibliografia
\newcommand{\estilobibliografico}[1]{ 
    \ifthenelse{\value{__usandoabnt} < 1}{
        \bibliographystyle{#1}
    }{}
}

%%%%%%%%%%%%%%%% RESUMO 
\renewenvironment{abstract}{
    \section*{\hfil\abstractname}
    \begin{quotation}
        \small\noindent
}{%
    \end{quotation}
    \bookmarksetup{startatroot} % fix bookmarks
}

%%%%%%%%%%%%%%%% TITULO
\def\@tipo{\empty}
\newcommand{\tipo}[1]{\def\@tipo{#1}}

\def\@titulo{\empty}
\renewcommand{\titulo}[1]{\def\@titulo{#1}}

\def\@aluno{\empty}
\newcommand{\aluno}[1]{\def\@aluno{#1}}

\def\@orientador{\empty}
\renewcommand{\orientador}[1]{\def\@orientador{#1}}

\def\@palavraschave{\empty}
\newcommand{\palavraschave}[1]{\def\@palavraschave{#1}}


\def\commonmaketitle{
    {\LARGE{\@tipo}}\\\vspace{0.814cm}
    {\LARGE\textbf\@titulo}\\\vspace{0.414cm}
    {\large{Aluna: \@aluno}}\\
    {\large{Orientador: \@orientador}}\\
}

\makeatletter
\def\maketitle{%
\begin{center}
    \commonmaketitle
    \normalfont
    \vspace{.6785cm}
\end{center}
}
\makeatother

%%%%%%%%%%%%%%%% METADADOS E LINKS
\makeatletter
    \AtBeginDocument{ %DEFINIÇÃO DE METADADOS APÓS AS VARIÁVEIS
        \hypersetup{
            pdftitle        = {\@titulo}, 
            pdfsubject      = {\@tipo},
            pdfcreator      = {LaTeX},
            pdfkeywords     = {\@palavraschave},
        }
    }
    \hypersetup{
        %draft,         % Desabilita links
        colorlinks      = true, % false:caixas; true:links coloridos
        linkcolor       = black, % Cor de links internos
        citecolor       = black, % Cor de links da bibliografia
        filecolor       = black, % Cor de links para arquivos
        urlcolor        = black, % Cor de url
        bookmarksdepth  = 4
    }
\makeatother
