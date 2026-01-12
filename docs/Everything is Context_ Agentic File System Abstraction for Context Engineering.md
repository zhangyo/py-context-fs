 Everything is Context: Agentic File System Abstraction for Context Engineering   

 [![logo](./Everything is Context_ Agentic File System Abstraction for Context Engineering_files/arxiv-logomark-small-white.svg) Back to arXiv](https://arxiv.org/)

[](https://arxiv.org/abs/2512.05470v1)[](javascript:toggleColorScheme() "Toggle dark/light mode")

 [![logo](./Everything is Context_ Agentic File System Abstraction for Context Engineering_files/arxiv-logo-one-color-white.svg) Back to arXiv](https://arxiv.org/)

This is **experimental HTML** to improve accessibility. We invite you to report rendering errors. Use Alt+Y to toggle on accessible reporting links and Alt+Shift+Y to toggle off. Learn more [about this project](https://info.arxiv.org/about/accessible_HTML.html) and [help improve conversions](https://info.arxiv.org/help/submit_latex_best_practices.html).

[Why HTML?](https://info.arxiv.org/about/accessible_HTML.html) [Report Issue](https://arxiv.org/html/2512.05470v1/#myForm) [Back to Abstract](https://arxiv.org/abs/2512.05470v1) [Download PDF](https://arxiv.org/pdf/2512.05470v1)[](javascript:toggleColorScheme() "Toggle dark/light mode")

Table of Contents
-----------------

1.  [Abstract](https://arxiv.org/html/2512.05470v1#abstract "Abstract")
2.  [I Introduction](https://arxiv.org/html/2512.05470v1#S1 "In Everything is Context: Agentic File System Abstraction for Context Engineering")
3.  [II Background and Related Work](https://arxiv.org/html/2512.05470v1#S2 "In Everything is Context: Agentic File System Abstraction for Context Engineering")
4.  [III File system as Infrastructure for Context](https://arxiv.org/html/2512.05470v1#S3 "In Everything is Context: Agentic File System Abstraction for Context Engineering")
    1.  [III-1 Abstraction](https://arxiv.org/html/2512.05470v1#S3.SS0.SSS1 "In III File system as Infrastructure for Context ‣ Everything is Context: Agentic File System Abstraction for Context Engineering")
    2.  [III-2 Modularity and Encapsulation](https://arxiv.org/html/2512.05470v1#S3.SS0.SSS2 "In III File system as Infrastructure for Context ‣ Everything is Context: Agentic File System Abstraction for Context Engineering")
    3.  [III-3 Separation of Concerns](https://arxiv.org/html/2512.05470v1#S3.SS0.SSS3 "In III File system as Infrastructure for Context ‣ Everything is Context: Agentic File System Abstraction for Context Engineering")
    4.  [III-4 Traceability and Verifiability](https://arxiv.org/html/2512.05470v1#S3.SS0.SSS4 "In III File system as Infrastructure for Context ‣ Everything is Context: Agentic File System Abstraction for Context Engineering")
    5.  [III-5 Composability and Evolvability](https://arxiv.org/html/2512.05470v1#S3.SS0.SSS5 "In III File system as Infrastructure for Context ‣ Everything is Context: Agentic File System Abstraction for Context Engineering")
5.  [IV Persistent Context Repository: History and Memory Lifecycle](https://arxiv.org/html/2512.05470v1#S4 "In Everything is Context: Agentic File System Abstraction for Context Engineering")
    1.  [IV-A History: Immutable Source of Truth](https://arxiv.org/html/2512.05470v1#S4.SS1 "In IV Persistent Context Repository: History and Memory Lifecycle ‣ Everything is Context: Agentic File System Abstraction for Context Engineering")
    2.  [IV-B Memory: Structured and Indexed Views](https://arxiv.org/html/2512.05470v1#S4.SS2 "In IV Persistent Context Repository: History and Memory Lifecycle ‣ Everything is Context: Agentic File System Abstraction for Context Engineering")
    3.  [IV-C Scratchpad: Temporary Workspace](https://arxiv.org/html/2512.05470v1#S4.SS3 "In IV Persistent Context Repository: History and Memory Lifecycle ‣ Everything is Context: Agentic File System Abstraction for Context Engineering")
    4.  [IV-D Governance](https://arxiv.org/html/2512.05470v1#S4.SS4 "In IV Persistent Context Repository: History and Memory Lifecycle ‣ Everything is Context: Agentic File System Abstraction for Context Engineering")
6.  [V Context Engineering Pipeline](https://arxiv.org/html/2512.05470v1#S5 "In Everything is Context: Agentic File System Abstraction for Context Engineering")
    1.  [V-A Design Constraints](https://arxiv.org/html/2512.05470v1#S5.SS1 "In V Context Engineering Pipeline ‣ Everything is Context: Agentic File System Abstraction for Context Engineering")
        1.  [V-A1 Token window](https://arxiv.org/html/2512.05470v1#S5.SS1.SSS1 "In V-A Design Constraints ‣ V Context Engineering Pipeline ‣ Everything is Context: Agentic File System Abstraction for Context Engineering")
        2.  [V-A2 Statelessness](https://arxiv.org/html/2512.05470v1#S5.SS1.SSS2 "In V-A Design Constraints ‣ V Context Engineering Pipeline ‣ Everything is Context: Agentic File System Abstraction for Context Engineering")
        3.  [V-A3 Non-Deterministic and Probabilistic Output](https://arxiv.org/html/2512.05470v1#S5.SS1.SSS3 "In V-A Design Constraints ‣ V Context Engineering Pipeline ‣ Everything is Context: Agentic File System Abstraction for Context Engineering")
    2.  [V-B Design of Context Engineering Pipeline](https://arxiv.org/html/2512.05470v1#S5.SS2 "In V Context Engineering Pipeline ‣ Everything is Context: Agentic File System Abstraction for Context Engineering")
        1.  [V-B1 Context Constructor](https://arxiv.org/html/2512.05470v1#S5.SS2.SSS1 "In V-B Design of Context Engineering Pipeline ‣ V Context Engineering Pipeline ‣ Everything is Context: Agentic File System Abstraction for Context Engineering")
        2.  [V-B2 Context Updater](https://arxiv.org/html/2512.05470v1#S5.SS2.SSS2 "In V-B Design of Context Engineering Pipeline ‣ V Context Engineering Pipeline ‣ Everything is Context: Agentic File System Abstraction for Context Engineering")
        3.  [V-B3 Context Evaluator](https://arxiv.org/html/2512.05470v1#S5.SS2.SSS3 "In V-B Design of Context Engineering Pipeline ‣ V Context Engineering Pipeline ‣ Everything is Context: Agentic File System Abstraction for Context Engineering")
7.  [VI Implementation Platform: AIGNE Framework](https://arxiv.org/html/2512.05470v1#S6 "In Everything is Context: Agentic File System Abstraction for Context Engineering")
    1.  [VI-A Exemplar 1: Memory-Enabled Context Construction](https://arxiv.org/html/2512.05470v1#S6.SS1 "In VI Implementation Platform: AIGNE Framework ‣ Everything is Context: Agentic File System Abstraction for Context Engineering")
    2.  [VI-B Exemplar 2: MCP with Github](https://arxiv.org/html/2512.05470v1#S6.SS2 "In VI Implementation Platform: AIGNE Framework ‣ Everything is Context: Agentic File System Abstraction for Context Engineering")
8.  [VII Conclusion and Future Work](https://arxiv.org/html/2512.05470v1#S7 "In Everything is Context: Agentic File System Abstraction for Context Engineering")

[License: arXiv.org perpetual non-exclusive license](https://info.arxiv.org/help/license/index.html#licenses-available)

arXiv:2512.05470v1 \[cs.SE\] 05 Dec 2025

Everything is Context: Agentic File System  
Abstraction for Context Engineering  

===================================================================================

Report issue for preceding element

Xiwei Xu  
Xuewu Gu    Robert Mao  
Yechao Li    Quan Bai  
Liming Zhu

Report issue for preceding element

###### Abstract

Report issue for preceding element

Generative AI (GenAI) has reshaped software system design by introducing foundation models as pre-trained subsystems that redefine architectures and operations. The emerging challenge is no longer model fine-tuning but context engineering—how systems capture, structure, and govern external knowledge, memory, tools, and human input to enable trustworthy reasoning. Existing practices such as prompt engineering, retrieval-augmented generation (RAG), and tool integration remain fragmented, producing transient artefacts that limit traceability and accountability. This paper proposes a file-system abstraction for context engineering, inspired by the Unix notion that “everything is a file.” The abstraction offers a persistent, governed infrastructure for managing heterogeneous context artefacts through uniform mounting, metadata, and access control. Implemented within the open-source AIGNE framework, the architecture realises a verifiable context-engineering pipeline, comprising the Context Constructor, Loader, and Evaluator, that assembles, delivers, and validates context under token constraints. As GenAI becomes an active collaborator in decision support, humans play a central role as curators, verifiers, and co-reasoners. The proposed architecture establishes a reusable foundation for accountable and human-centred AI co-work, demonstrated through two exemplars: an agent with memory and an MCP-based GitHub assistant. The implementation within the AIGNE framework demonstrates how the architecture can be operationalised in developer and industrial settings, supporting verifiable, maintainable, and industry-ready GenAI systems.

Report issue for preceding element

I Introduction
--------------

Report issue for preceding element

Context engineering is emerging as a central concern in software architecture for Generative AI (GenAI) and Agentic systems\[bleigh2025context, mei2025surveycontextengineeringlarge, LangChainContextEngineering2024\]. It refers to the process of capturing, structuring, and governing external knowledge, memory, tools, and human input so that reasoning by large language models (LLMs) and agents is grounded in the right information, constraints, and provenance. In contrast to prompt engineering, which focuses on crafting individual instructions, context engineering focuses on the entire information lifecycle, from selection, retrieval, filtering, construction, to compression, evaluation and refresh, ensuring that GenAI systems and agents remain coherent, efficient, and verifiable over time.

Report issue for preceding element

Recent industrial frameworks such as LangChain have begun to articulate context engineering as a structured process within agent architectures \[LangChainContextEngineering2024\]. Four key stages of context engineering are identified. Agents first write contextual information into a shared memory or store, select the most relevant elements for a given task, compress the selected context to fit model constraints, and isolate the final subset across agents for reasoning. These industrial practices highlight the growing recognition that context management has become a central architectural concern. Similar pipelines appear in AutoGen \[AutoGenMemory2024\], and other related frameworks that support tool use and memory augmentation \[AnthropicContextEngineering2024\]. However, these solutions remain ad hoc and implementation-driven. They lack a unified architectural foundation to ensure traceability, governance, or systematic handling of evolving context. Consequently, context artefacts generated during these steps are often transient, opaque, and unverifiable, raising challenges of context rot \[TrychromaContextRot2024\] and knowledge drift in industrial-setting GenAI systems \[laban2025llmslostmultiturnconversation\].

Report issue for preceding element

GenAI introduces new architectural constraints in AI engineering \[SAML\]. Foundation models act as pre-trained subsystems with limited token windows that constrain reasoning. This bounded working memory propagates upward through the architecture, shaping how context must be selected, modularised, compressed, and loaded at runtime. As GenAI becomes an active collaborator across domains such as education, healthcare, and decision support, humans increasingly co-work with AI \[RAGHuman, xu2025ragopsoperatingmanagingretrievalaugmented\] on reasoning and decision-making tasks. Yet GenAI systems may produce inaccurate or misleading outputs due to limited contextual awareness and evolving data sources. Architectural mechanisms are therefore needed to govern how persistent knowledge (long-term memory) transitions into bounded context (short-term window) in a traceable, verifiable, and human-aware manner, ensures that human judgment and tacit knowledge remain embedded within the system’s evolving context for reasoning and evaluation.

Report issue for preceding element

This paper introduces a file-system abstraction as an architectural foundation, as a stepping stone for context engineering, inspired by the Unix philosophy that “everything is a file”\[Unix\]. The abstraction provides a persistent, hierarchical, and governed environment where heterogeneous context sources, such as memory, tools, external knowledge, and human contributions, are mounted and accessed uniformly. Building upon this infrastructure, the paper extends file system into a context-engineering pipeline that operationalises context construction under explicit architectural design constraints with the token window. The pipeline performs selection, compression, and incremental streaming of context to ensure that bounded context capacity is used efficiently and transparently.

Report issue for preceding element

Section [II](https://arxiv.org/html/2512.05470v1#S2 "II Background and Related Work ‣ Everything is Context: Agentic File System Abstraction for Context Engineering") reviews related developments in SE4AI and motivates the need for architectural foundations for context engineering. Section [III](https://arxiv.org/html/2512.05470v1#S3 "III File system as Infrastructure for Context ‣ Everything is Context: Agentic File System Abstraction for Context Engineering") introduces the file system abstraction and its role as a persistent context infrastructure. Section [V](https://arxiv.org/html/2512.05470v1#S5 "V Context Engineering Pipeline ‣ Everything is Context: Agentic File System Abstraction for Context Engineering") introduces the design constraints and presents the context-engineering pipeline built on these constraints. Section [VI](https://arxiv.org/html/2512.05470v1#S6 "VI Implementation Platform: AIGNE Framework ‣ Everything is Context: Agentic File System Abstraction for Context Engineering") details the AIGNE implementation of the proposed file system abstraction, illustrated through two exemplars. Finally, Section [VII](https://arxiv.org/html/2512.05470v1#S7 "VII Conclusion and Future Work ‣ Everything is Context: Agentic File System Abstraction for Context Engineering") discusses key challenges, future research directions, and concluding remarks.

Report issue for preceding element

II Background and Related Work
------------------------------

Report issue for preceding element

The emergence of agentic Generative AI systems has given rise to an operating-system paradigm for LLMs (LLM-as-OS), which conceptualises the LLM as a kernel orchestrating context, memory, tools, and agents. AIOS project \[ge2023llmosagentsapps\] operationalises this paradigm through OS-like primitives for scheduling, resource allocation, and memory management for multi-agent systems \[mei2025aiosllmagentoperating\]. Recent work on further extends this view by proposing an LLM-based semantic file system that enables natural-language–driven file operations and semantic indexing \[shi2025lsfs\] MemGPT \[packer2024memgptllmsoperatingsystems\] introduces a memory hierarchy that coordinates both short-term (context window) and long-term (external storage) memory. While the LLM-as-OS paradigm provides an intuitive high-level conceptual model, it lacks a software-architectural abstraction for how context is structured, shared, and governed. In particular, existing implementations often treat memory, retrieval, and tool use as independent components rather than a coherent infrastructure.

Report issue for preceding element

In parallel, context engineering\[LangChainContextEngineering2024, hua2025contextengineering20context\] has emerged as a central element in design of Generative AI system. Unlike traditional prompt engineering, which considers context as just a fixed block of text, context engineering treats it as a living, structured mix of instructions, external knowledge, tool definitions, memory, system state, and user queries. Frameworks such as LangChain \[LangChainDeepAgents2025\], AutoGen \[AutoGenMemory2024\] provide partial support through modular components for memory and tool orchestration, but they lack unified mechanisms for traceability, governance, and lifecycle management of context artefacts. Emerging link-based mechanisms \[bleigh2025context\] treats context as interconnected, discoverable resources, highlighting the need for an unified, verifiable infrastructure to manage such dynamic context. Recent survey \[mei2025surveycontextengineeringlarge\] from academia also confirms that current approaches are fragmented and identified gaps in verification and lifecycle support. An integrated framework is proposed for bridging context construction and retrieval \[dai2025onepiecebringingcontextengineering\] but note the absence of a verifiable architectural foundation.

Report issue for preceding element

Industry and open-source efforts have converged on long-term memory as a critical capability for agentic systems. Existing solutions can be roughly categorized into embedding based solutions, like mem0 \[mem0\] and Letta (formerly MemGPT) \[LettaAI2025\], and Knowledge Graph (KG) based solutions, like Zep/Graphiti \[rasmussen2025zeptemporalknowledgegraph\] and Cognee \[markovic2025optimizinginterfaceknowledgegraphs\]. However, across these solutions, context governance, access control, and multi-agent sharing remain largely ad hoc. Most frameworks focus on storage and retrieval optimization rather than architectural composability or verifiable traceability.

Report issue for preceding element

Beyond architectural paradigms, growing attention has been paid to the dynamics of human–AI co-work, where humans and AI agents jointly perform reasoning, assessment, and decision-making tasks. Recent studies show that combining human judgment with AI inference can enhance performance when tasks require contextual understanding, ethical reasoning, or tacit domain knowledge \[designRAG, Lindner2024HumanAICollaboration, CHI2019\].

Report issue for preceding element

The file system abstraction proposed in this paper aligns with the broader LLM-as-OS paradigm. It provides a persistent and governed infrastructure for mounting and managing heterogeneous context resources. By aligning with core software-architectural principles, including modularity, encapsulation, separation of concerns, and traceability, the file system transforms context engineering from ad hoc practice into a systematic, verifiable, and reusable infrastructure. Human roles are directly embed into the context-engineering architecture, ensuring that tacit knowledge and ethical judgment remain integral parts of system reasoning and evaluation.

Report issue for preceding element

III File system as Infrastructure for Context
---------------------------------------------

Report issue for preceding element

The file system provides the foundational infrastructure that enables systematic context engineering in GenAI systems.Within this environment, agents and human experts function analogously to operating-system processes, performing file-style operations such as reading, writing, and searching on mounted context resources. The file system defines a uniform namespace and a consistent set of basic operations that together enable scalable coordination between autonomous and human actors. The overall architecture of the proposed infrastructure is represented in Figure [1](https://arxiv.org/html/2512.05470v1#S3.F1 "Figure 1 ‣ III File system as Infrastructure for Context ‣ Everything is Context: Agentic File System Abstraction for Context Engineering"). This architectural abstraction aligns with established software engineering first principles. Concepts such as abstraction, modularity, encapsulation, separation of concerns, and composability shape how context resources are represented, accessed, and evolved. By applying these principles, the file system transforms the complexity of heterogeneous context into a structured, verifiable, and extensible environment for human–AI co-work. The file system operationalises LLM-as-Operating-System paradigm by transforming the metaphor into a concrete software architecture design.

Report issue for preceding element

![Refer to caption](./Everything is Context_ Agentic File System Abstraction for Context Engineering_files/architecture.png)

Report issue for preceding element

Figure 1: File system as a unifying abstraction for context engineering.

Report issue for preceding element

#### III-1 Abstraction

Report issue for preceding element

The file system implements the SE principle of abstraction, providing a uniform interface that hides the heterogeneity of underlying context sources. Regardless of whether a resource is a knowledge graph, a memory store, or a human-curated note, it is represented through a standardised file interface. Because the file system is schema-driven, heterogeneous structures—including REST/OpenAPI resources, GraphQL types, MCP tools, memory stores, or external APIs—can be automatically projected into the namespace. This avoids integration code and turns the file system into a universal semantic interface. This allows agents to reason over diverse context types without knowing their physical format, storage mechanism, or retrieval logic.

Report issue for preceding element

#### III-2 Modularity and Encapsulation

Report issue for preceding element

The architecture realizes modularity by decomposing the environment into independently manageable context resources. Each resource is encapsulated as a mounted component with well-defined boundaries and metadata. This encapsulation isolates the internal logic or backend implementation of each resource while exposing only the minimal set of operations required for integration. Thus, changes in one component, for example, swapping a relational database for a vector store, do not propagate across other components in the system. These capabilities eliminate the need to hard-code extensive tool descriptions that would otherwise overload the model’s token window. New context sources can be mounted dynamically, similar to Unix file systems, allowing agents to treat external services, tools, or databases as part of a unified addressable space.

Report issue for preceding element

#### III-3 Separation of Concerns

Report issue for preceding element

Following the SE principle of separation of concerns, the file system distinguishes between data, tools, and governance layers. Non-executable files, such as config.yaml or experiment\_results.csv, serve as data or knowledge resources, while executable artefacts such as analyser.py or simulate.sh represent active tools. This clear distinction ensures that agents and human experts can interpret intent and behaviour correctly, applying appropriate verification and execution strategies. Separation of concerns also extends to governance: access control, log, and metadata management are handled through dedicated mechanisms that remain independent of the functional logic of retrieval or reasoning.

Report issue for preceding element

#### III-4 Traceability and Verifiability

Report issue for preceding element

Every interaction with the file system, whether initiated by an agent or a human, is logged as a transaction in the persistent context repository. This enforces traceability that enables the reconstruction of context provenance and accountability of actions. Coupled with structured metadata, these logs support verifiability by allowing changes, reasoning steps, and tool invocations to be audited retrospectively. This ensures that the context pipeline is not only functional but also transparent and auditable.

Report issue for preceding element

#### III-5 Composability and Evolvability

Report issue for preceding element

The file system achieves composability by defining a consistent namespace and interoperable metadata schema across all mounted resources. Context elements can be combined, queried, or integrated into higher-level reasoning processes without additional integration code. Evolvability is realised through a plugin architecture that allows new backends, such as full-text indexers, vector databases, or knowledge graphs to be mounted seamlessly without modifying the other components.

Report issue for preceding element

Beyond standard file operations, the abstraction can associate each file or directory with meta-defined actions. These actions specify callable behaviours discoverable by agents, ranging from analytical functions, including summarisation, validation, and synchronisation, to domain-specific transformations. Actions elevate each file or directory into an active node, allowing agents to execute tools, transformations or service calls directly through the file system interface.

Report issue for preceding element

IV Persistent Context Repository: History and Memory Lifecycle
--------------------------------------------------------------

Report issue for preceding element

Large language models are inherently stateless: once a session ends, all contextual information is lost. To sustain coherent reasoning across sessions, a GenAI system requires an external, persistent memory repository that captures, structures, and evolves context over time. The Persistent Context Repository enabled by the File System fulfills this role. It unifies history, memory, and scratchpad into a continuous lifecycle, ensuring that both short-term and long-term contextual knowledge remain accessible, traceable, and up to date.

Report issue for preceding element

When an interaction occurs, raw data are first appended to History. Summarisation, embedding and indexing transforms these records into Memory representations optimized for retrieval and reasoning. During reasoning, temporary information are written to Scratchpads, which may be selectively inserted into Memory or archived in History after validation. This layered design ensures that all context resources remain both traceable and reusable across agents and sessions.

Report issue for preceding element

![Refer to caption](./Everything is Context_ Agentic File System Abstraction for Context Engineering_files/HistoryMemory.png)

Report issue for preceding element

Figure 2: Lifecycle of History, Memory and Scratchpad

Report issue for preceding element

These components differ in persistence: history is global and permanent; memory is agent-specific or session-specific, persistent but mutable; and scratchpads are transient yet auditable. Short-term context, assembled dynamically within the model’s token window, functions like working memory. Long-term context, by contrast, must reside outside the model and be selectively included when needed.

Report issue for preceding element

The file system enables provenance through timestamps, version control, and access policies. Each transformation, from history to memory, or from scratchpad to memory, is logged as a verifiable state transition. Each artefact carries its creation context, ownership, and lineage, enabling verifiable reconstruction of the reasoning process. This makes the repository not only a data store but also a traceability infrastructure that aligns context management with software engineering principles of modularity and traceability.

Report issue for preceding element

### IV-A History: Immutable Source of Truth

Report issue for preceding element

History records all raw interactions between users, agents, and the environment. Each input, output, and intermediate reasoning step is logged immutable and enriched with metadata such as timestamp, origin, and model version. History acts as a verifiable source of truth. It can span multiple agents and sessions, forming a shared global data record accessible through the file system namespace (e.g., /context/history/). By maintaining complete traces, the system preserves the provenance of reasoning and enables post-hoc analysis, debugging, and compliance verification.

Report issue for preceding element

### IV-B Memory: Structured and Indexed Views

Report issue for preceding element

From the context management perspective, memory can be classified along temporal, structural, and representational dimensions.

Report issue for preceding element

*   •
    
    Temporal: How long the memory persists.
    
    Report issue for preceding element
    
*   •
    
    Structural: Size or abstraction level of what’s stored, token-level, fact-level, or summary-level.
    
    Report issue for preceding element
    
*   •
    
    Representational: How the memory is modelled internally, as raw text, vector embeddings, structured triples, or summaries.
    
    Report issue for preceding element
    

While the short-term versus long-term distinction originates from human cognition, practical GenAI systems manage a spectrum of memory types that balance persistence with dynamism \[wang2024limitssurveytechniquesextend\], such as episodic memory (task-bounded summaries) and fact memory (persistent atomic facts). Semantic or induced memory captures higher-level embeddings derived from clustering or summarisation. Each type serves a complementary role within the GenAI reasoning process, ranging from ephemeral reasoning support to enduring knowledge preservation, and is exposed through a consistent namespace hierarchy. Multiple memory types may coexist, as illustrated in Table [I](https://arxiv.org/html/2512.05470v1#S4.T1 "TABLE I ‣ IV-B Memory: Structured and Indexed Views ‣ IV Persistent Context Repository: History and Memory Lifecycle ‣ Everything is Context: Agentic File System Abstraction for Context Engineering").

Report issue for preceding element

Memory entries are agent-specific and governed through shared metadata and access-control rules. Each memory item maintains a reference to its historical source, ensuring traceability between summarized and original data. Indexed logs and embeddings enable selective recall without re-scanning the entire history, supporting performance and scalability. In the file system, memory is exposed as /context/memory/agentID and can be extended through plugins such as vector databases or full-text search engines.

Report issue for preceding element

TABLE I: Taxonomy of Memory Types in Context Engineering

Memory Type

Temporal Scope

Structural Unit

Representation

Scratchpad

Temporary, task-bounded

Dialogue turns, temporary reasoning states

Plain text or embeddings

Episodic Memory

Medium-term, session-bounded

Session summaries, case histories

Summaries in plain text or embeddings

Fact Memory

Long-term, fine-grained

Atomic factual statements

Key–value pairs or triples

Experiential Memory

Long-term, cross-task

Observation-action trajectories

Structured logs or database

Procedural Memory

Long-term, system-wide

Functions, tools, or function definitions

API or code references

User Memory

Long-term, personalized

User attributes, preferences and histories

User profiles, embeddings

Historical Record

Immutable, full-trace

Raw logs of all interactions

Plain text with metadata

Report issue for preceding element

### IV-C Scratchpad: Temporary Workspace

Report issue for preceding element

Scratchpads serve as temporary workspaces where agents compose intermediate hypotheses, computations, or drafts during reasoning. Unlike memory, scratchpads are ephemeral and scoped to a specific task or reasoning episode. However, once a session concludes, relevant artefacts may be inserted into memory or appended to history, completing the loop. Scratchpads are represented in the file system as /context/pad/taskID and are governed by the same metadata and access-control schema as persistent artefacts.

Report issue for preceding element

### IV-D Governance

Report issue for preceding element

The lifecycle of history/memory/scratchpad is governed by explicit policies for versioning, aging, and retention. For example, obsolete scratchpads can be pruned automatically, while historical logs may be compressed but never deleted. Such policies ensure that the system remains both scalable and auditable. The persistent context repository operates as a mounted layer within the file system, using its hierarchical namespace and access-control mechanisms. It also serves as the principal data source for the context engineering pipeline, where selected memory and history artefacts are retrieved, compressed, and injected into the context constrained by the token window. All state transitions and transformations are represented as file-level events with timestamps and lineage metadata, enabling replay, audit, and reversible evolution.

Report issue for preceding element

V Context Engineering Pipeline
------------------------------

Report issue for preceding element

### V-A Design Constraints

Report issue for preceding element

GenAI model introduce a unique set of architectural design constraints that collectively define the rationale for the design of the context engineering pipeline, fundamentally shape how context is operated. These constraints are intrinsic to the GenAI model layer, and cascade upward through the software architecture, influencing the structure and behavior of higher-level components. Recognizing and formalizing these design constraints transforms context engineering from ad-hoc prompting practices into a systematic software-architectural discipline.

Report issue for preceding element

#### V-A1 Token window

Report issue for preceding element

The token window of GenAI model introduces a hard architectural constraint, which defines the maximum number of tokens that the model can attend to during a single inference pass. This bounded reasoning capacity, determined by model architecture, sets an upper limit on the amount of active context available at runtime (e.g., 128K for GPT 5111https://platform.openai.com/docs/models/gpt-5-chat-latest, 200k for Claude Sonnet 4.5222https://www.anthropic.com/claude/sonnet). Moreover, as the length of input prompts increases, the computational cost of GenAI models rises significantly due to the quadratic complexity of the self-attention mechanism \[pmlr-v201-duman-keles23a\].

Report issue for preceding element

Consequently, the context engineering pipeline must curate, compress, and incrementally stream relevant information from the file system into the model’s token window. Persistent information in memory must therefore be modularized and hierarchically organized, enabling selective retrieval and incremental refresh. The pipeline manages the temporal coherence of the active window, ensuring that reasoning remains consistent and traceable within bounded context limit. The simplest mitigation is to truncate or summarise large texts, though this inevitably risks information loss \[wang2024limitssurveytechniquesextend\].

Report issue for preceding element

#### V-A2 Statelessness

Report issue for preceding element

GenAI models are inherently stateless, which do not retain conversational history or memory across sessions. This constraint requires external persistent context repository that records, reconstructs, and governs relevant information across interactions. The stateless nature also drives the need for the session memory mechanisms to restore continuity and avoid redundant computation.

Report issue for preceding element

However, persisting state externally introduces secondary challenges related to memory growth and redundancy. As conversational or task histories accumulate, semantically similar entries or repeated experiences can increase quickly, degrading retrieval precision and increasing storage cost. To mitigate these effects, context engineering pipeline requires memory deduplication and consolidation strategies that maintain a memory base with minimal redundancy.

Report issue for preceding element

#### V-A3 Non-Deterministic and Probabilistic Output

Report issue for preceding element

Because LLMs produce probabilistic outputs conditioned on sampling parameters (e.g., temperature), identical prompts can yield varying responses. From an architectural perspective, this non-determinism introduces challenges for traceability, testing, and verification. It is required that the context engineering pipeline preserves input–output pairs, metadata, and provenance within the file system to support audit, replay, and post-hoc evaluation.

Report issue for preceding element

### V-B Design of Context Engineering Pipeline

Report issue for preceding element

Building upon the unified architectural foundation established by the file system, this section proposes Context Engineering Pipeline that serves as the operational layer that orchestrates context evolution across components.

Report issue for preceding element

A pipeline that retains context through both long-term and short-term mechanisms is a key component of an autonomous GenAI agent \[castrillo2025fundamentalsbuildingautonomousllm\]. Such a pipeline keeps the knowledge and context that is not embedded within the model’s weights. The Context Engineering Pipeline bridges context stored in the persistent context repository (history, memory, tools, human input) with bounded reasoning (the token window), ensuring that context is continuously constructed, refreshed, and evaluated throughout the operational lifecycle of an agent. Architecturally, as shown in Figure [3](https://arxiv.org/html/2512.05470v1#S5.F3 "Figure 3 ‣ V-B Design of Context Engineering Pipeline ‣ V Context Engineering Pipeline ‣ Everything is Context: Agentic File System Abstraction for Context Engineering"), the pipeline consists of three components: the Context Constructor, the Context Updater, and the Context Evaluator. The architecture operates under three interrelated design constraints as discussed in Section [V-A](https://arxiv.org/html/2512.05470v1#S5.SS1 "V-A Design Constraints ‣ V Context Engineering Pipeline ‣ Everything is Context: Agentic File System Abstraction for Context Engineering"). The pipeline performs selection, compression, injection, refreshing, and human-in-the-loop evaluation and overwrite, forming a closed loop for context management. Metadata in the file system is used by all the major operations in the context engineering pipeline.

Report issue for preceding element

![Refer to caption](./Everything is Context_ Agentic File System Abstraction for Context Engineering_files/pipeline.png)

Report issue for preceding element

Figure 3: The Context Engineering Pipeline.

Report issue for preceding element

#### V-B1 Context Constructor

Report issue for preceding element

The Constructor defines how relevant context is selected, prioritized, and compressed from the persistent context repository to prepare bounded, task-specific inputs for reasoning. This process transforms unbounded knowledge into a curated subset that is suitable for the model’s active context window. Context selection must also fulfill non-functional qualities such as privacy, access control, and data governance. Because the file system serves as a shared global infrastructure across agents and tasks, the Constructor enforces these constraints to ensure that each reasoning session operates within its authorized scope and the corresponding context remains properly isolated.

Report issue for preceding element

Architecturally, the Constructor manages a trade-off between completeness (covering all relevant information) with boundedness (respecting token constraint and cost efficiency). It relies on metadata indicating recency, provenance, which together help infer the relevance of context elements during retrieval and prioritization. Selected context is then compressed through summarization, embedding, or clustering techniques to meet computational budgets, before being aligned with the model’s prompt schema \[white2023promptpatterncatalogenhance, 10.1145/3560815\], a structured input format specifying how context elements are organized for inference.

Report issue for preceding element

The Constructor interfaces directly with the file system mount points (e.g., /context/memory/, /context/tool/), queries metadata, and generates a context manifest that records which elements were selected, excluded, and why. This manifest provides transparency, reproducibility, and verifiability for each reasoning session, turning context assembly from an ad hoc operation into a traceable architectural process.

Report issue for preceding element

#### V-B2 Context Updater

Report issue for preceding element

The Context Updater manages the transfer and refresh of constructed context into the bounded reasoning space of the GenAI model. Given the model’s limited token window, the Updater must continuously synchronize the token window, the state of the persistent context repository, and the runtime dialogue to maintain coherence and consistency. It ensures that the active context always reflects the most relevant and authorized information, without exceeding model limits or violating access and governance constraints. This synchronization requires continuous monitoring of context size, relevance decay, and temporal and structural dependencies across agents and sessions.

Report issue for preceding element

At beginning of the process, a static snapshot of context may be fed into before a single reasoning task for processing. During extended reasoning, incremental streaming allows additional fragments of context to be progressively loaded as the reasoning unfolds. In dynamic or interactive sessions, adaptive refresh mechanisms replace outdated or less relevant fragments in response to model feedback or human intervention. Together, these modes collectively ensure that the reasoning process remains contextually grounded.

Report issue for preceding element

All context loading and replacement actions are recorded as metadata events within the file system, including timestamps, source paths, and reasoning identifiers, to enable full traceability and replay of any reasoning session. In multi-agent scenarios, the Context Updater also enforces resource isolation and access separation, ensuring that the context of one reasoning process neither interferes with nor leaks into another.

Report issue for preceding element

#### V-B3 Context Evaluator

Report issue for preceding element

The Context Evaluator closes the loop by verifying model outputs, updating the persistent context repository, and maintaining governance over the evolving knowledge base. It ensures that newly generated or refined information is validated, contextualized, and reintegrated into the persistent context repository in a traceable and auditable manner.

Report issue for preceding element

Model outputs are evaluated against their source context element and provenance metadata to detect hallucinations, contradictions, or context drift. This may involve automated semantic comparison, factual consistency checking, or cross-referencing with authoritative sources. Evaluation metrics, such as confidence scores, factual alignment, and human override rates, are recorded as structured metadata within the file system, supporting post-hoc analysis and traceability.

Report issue for preceding element

Verified outputs are transformed into structured memory element, updating or extending the persistent context repository. Long-term memory entries may be appended, revised, or summarized, while episodic memories and scratchpads are pruned or archived. Each update is versioned with timestamps and lineage metadata, ensuring that context evolution remains transparent and reversible.

Report issue for preceding element

When confidence thresholds are low or contradictions are detected, the Evaluator triggers human review. Human annotations, ranging from factual corrections to interpretive insights, are stored as explicit context elements, elevating tacit knowledge becomes a first-class component of the knowledge base.

Report issue for preceding element

VI Implementation Platform: AIGNE Framework
-------------------------------------------

Report issue for preceding element

The proposed file system and context engineering pipeline are implemented within the AIGNE Framework333https://github.com/AIGNE-io/aigne-framework, a functional development framework designed to simplify and accelerate the creation of GenAI agents. AIGNE provides native integration with multiple mainstream large language models (e.g., OpenAI, Gemini, Claude, DeepSeek, Ollama) and external services via the built-in Model Context Protocol (MCP), enabling dynamic and context-aware application behaviour.

Report issue for preceding element

In the AIGNE framework, the AFS (Agentic File System) module serves as the primary file system interface. The SystemFS module implements a virtual file system that provides the following key features.

Report issue for preceding element

*   •
    
    Supports list, read, write, and search commands for managing files within mounted directories.
    
    Report issue for preceding element
    
*   •
    
    Enables navigation across nested subdirectories with configurable depth limits.
    
    Report issue for preceding element
    
*   •
    
    Integrates with ripgrep for efficient content search.
    
    Report issue for preceding element
    
*   •
    
    Access to file timestamps, sizes, types, and support user-defined metadata
    
    Report issue for preceding element
    
*   •
    
    Sandboxed access restricted to mounted directories, ensuring isolation and secure file operation
    
    Report issue for preceding element
    

All mounted resources, including MCP modules, memory stores, databases, or external APIs, are projected into the file system through programmable resolvers. These resolvers implement declarative mappings (similar to GraphQL/OpenAPI schemas) that translate internal structures into AFS nodes without requiring any change to the underlying storage format, enabling semless integration of heterogenous systems.

Report issue for preceding element

Within AIGNE, context elements are represented as typed resources under the AFS namespace. Modules such as SystemFS, FSMemory, and UserProfileMemory, each exposing list/read/write/search APIs through standard asynchronous methods. This abstraction enables GenAI agents to access heterogeneous data, like local files, chat histories, and structured memory entries—through a uniform interface without concern for underlying storage backends.

Report issue for preceding element

In AIGNE, agents perform reasoning while delegating execution to modular Functions, which are implemented as executable files (e.g., Node.js modules). Each function exports a default asynchronous function together with metadata descriptors (description, input\_schema, and output\_schema) that allow agents to discover, validate, and invoke them with structured arguments. Functions act as the tools through which agents perform concrete actions, executing code in a sandbox, or calling external APIs.

Report issue for preceding element

The Context Constructor is implemented as a process. When a new prompt is received, The constructor executes a series of tool calls such as afs\_list() and afs\_read(), collecting candidate artefacts (documents, history records, or profile summaries) tagged with metadata including timestamps, provenance, and access scope. The constructor then applies summarisation and token-budget estimation functions to produce a JSON-formatted manifest, which records the selected artefacts, their ordering, and their estimated contribution to the model’s prompt. This manifest is passed downstream to the Context Updater.

Report issue for preceding element

The Context Updater is realised as part of AIGNE’s agent workflow engine. The updater streams context fragments into the model’s input buffer during dialogue. In single-turn tasks, it performs a one-off injection of a static snapshot; in interactive sessions, it incrementally refreshes the prompt by invoking AFS read operations to replace or append elements as reasoning unfolds.

Report issue for preceding element

The Context Evaluator leverages AIGNE’s memory modules to persist newly generated information. After each model response, validated outputs, like summarised user preferences or extracted factual statements, are written back to AFS, stored under directories such as /context/memory/fact/. Each entry is enriched with lineage metadata (createdAt, sourceId, confidence, and revisionId) to support audit and rollback. When the Evaluator detects uncertainty (e.g., confidence below threshold or inconsistent information), it triggers a human-verification stage: annotations are appended as separate artefacts in /context/human/.

Report issue for preceding element

### VI-A Exemplar 1: Memory-Enabled Context Construction

Report issue for preceding element

AIGNE enables agents to maintain contextual coherence across multiple dialogue turns. Memory is activated declaratively during agent construction through the DefaultMemory module, which persists conversation history as retrievable context. The storage location is specified as a file path (e.g., file:./memory.sqlite3), allowing memory data to be saved and reloaded across sessions. Each dialogue round is appended to memory and automatically incorporated into subsequent reasoning, enabling long-term, stateful interaction without explicit state management.

Report issue for preceding element

[⬇](data:text/plain;base64,aW1wb3J0IHsgQUlBZ2VudCB9IGZyb20gIkBhaWduZS9jb3JlIjsKaW1wb3J0IHsgQUZTIH0gZnJvbSAiQGFpZ25lL2FmcyI7CmltcG9ydCB7IEFGU0hpc3RvcnkgfSBmcm9tICJAYWlnbmUvYWZzLWhpc3RvcnkiOwppbXBvcnQgeyBVc2VyUHJvZmlsZU1lbW9yeSB9IGZyb20gIkBhaWduZS9hZnMtdXNlci1wcm9maWxlLW1lbW9yeSI7Cgpjb25zdCBzaGFyZWRTdG9yYWdlID0geyB1cmw6ICJmaWxlOi4vbWVtb3J5LnNxbGl0ZTMiIH07IC8vIHVzZSBhIFNRTGl0ZSBkYXRhYmFzZSBhcyBtZW1vcnkgc3RvcmFnZSBwcm92aWRlcgoKY29uc3QgYWZzID0gbmV3IEFGUygpCiAgLm1vdW50KG5ldyBBRlNIaXN0b3J5KHsgc3RvcmFnZTogc2hhcmVkU3RvcmFnZSB9KSkgIC8vIG1lc3NhZ2UgaGlzdG9yeSBtZW1vcnkKICAubW91bnQobmV3IFVzZXJQcm9maWxlTWVtb3J5KHsgc3RvcmFnZTogc2hhcmVkU3RvcmFnZSwgY29udGV4dDogYWlnbmUubmV3Q29udGV4dCgpIH0pKTsgLy8gdXNlciBtZW1vcnkKCmNvbnN0IGFnZW50ID0gQUlBZ2VudC5mcm9tKHsKICBpbnN0cnVjdGlvbnM6ICJZb3UgYXJlIGEgZnJpZW5kbHkgY2hhdGJvdCIsCiAgaW5wdXRLZXk6ICJtZXNzYWdlIiwKICBhZnMsCn0pOwo=)

1import { AIAgent } from "@aigne/core";

2import { AFS } from "@aigne/afs";

3import { AFSHistory } from "@aigne/afs-history";

4import { UserProfileMemory } from "@aigne/afs-user-profile-memory";

5

6const sharedStorage \= { url: "file:./memory.sqlite3" }; // use a SQLite database as memory storage provider

7

8const afs \= new AFS()

9 .mount(new AFSHistory({ storage: sharedStorage })) // message history memory

10 .mount(new UserProfileMemory({ storage: sharedStorage, context: aigne.newContext() })); // user memory

11

12const agent \= AIAgent.from({

13 instructions: "You are a friendly chatbot",

14 inputKey: "message",

15 afs,

16});

Listing 1: Defining an agent with persistent memory.

Report issue for preceding element

### VI-B Exemplar 2: MCP with Github

Report issue for preceding element

The second exemplar demonstrates that any MCP (Model Context Protocol) server can be mounted as an AFS module, exposing its capabilities through a unified file system interface. Using the GitHub MCP server as a real-world case, it shows AI agents interact with GitHub as if they were simply accessing files. Once mounted, the agent can invoke all GitHub MCP tools directly, using afs\_exec on /modules/github-mcp/search\_repositories and /modules/github-mcp/list\_issues.

Report issue for preceding element

[⬇](data:text/plain;base64,aW1wb3J0IHsgQUlBZ2VudCB9IGZyb20gIkBhaWduZS9jb3JlIjsKaW1wb3J0IHsgQUZTIH0gZnJvbSAiQGFpZ25lL2FmcyI7CmltcG9ydCB7IE1DUEFnZW50IH0gZnJvbSAiQGFpZ25lL2NvcmUiOwoKY29uc3QgbWNwQWdlbnQgPSBhd2FpdCBNQ1BBZ2VudC5mcm9tKHsgLy8gY3JlYXRlIGFnZW50IGZyb20gIEdpdEh1YiBvZmZpY2lhbCBNQ1AgU2VydmVyCiAgY29tbWFuZDogImRvY2tlciIsCiAgYXJnczogWwogICAgInJ1biIsICItaSIsICItLXJtIiwKICAgICItZSIsIGBHSVRIVUJfUEVSU09OQUxfQUNDRVNTX1RPS0VOPSR7cHJvY2Vzcy5lbnYuR0lUSFVCX1BFUlNPTkFMX0FDQ0VTU19UT0tFTn1gLAogICAgImdoY3IuaW8vZ2l0aHViL2dpdGh1Yi1tY3AiLAogIF0sCn0pOwoKY29uc3QgYWZzID0gbmV3IEFGUygpCi5tb3VudChtY3BBZ2VudCk7ICAvL01vdW50ZWQgYXQgL21vZHVsZXMvZ2l0aHViLW1jcAoKY29uc3QgYWdlbnQgPSBBSUFnZW50LmZyb20oewogIGluc3RydWN0aW9uczogIkhlbHAgdXNlcnMgaW50ZXJhY3Qgd2l0aCBHaXRIdWIgdmlhIHRoZSBnaXRodWItbWNwLXNlcnZlciBtb2R1bGUuIiwKICBpbnB1dEtleTogIm1lc3NhZ2UiLAogIGFmcywvL0FnZW50IGFjY2Vzc3MgdG8gYWxsIG1vdW50ZWQgbW9kdWxlc30pOwo=)

1import { AIAgent } from "@aigne/core";

2import { AFS } from "@aigne/afs";

3import { MCPAgent } from "@aigne/core";

4

5const mcpAgent \= await MCPAgent.from({ // create agent from GitHub official MCP Server

6 command: "docker",

7 args: \[

8 "run", "-i", "--rm",

9 "-e", ‘GITHUB\_PERSONAL\_ACCESS\_TOKEN\=${process.env.GITHUB\_PERSONAL\_ACCESS\_TOKEN}‘,

10 "ghcr.io/github/github-mcp",

11 \],

12});

13

14const afs \= new AFS()

15.mount(mcpAgent); //Mounted at /modules/github-mcp

16

17const agent \= AIAgent.from({

18 instructions: "Help users interact with GitHub via the github-mcp-server module.",

19 inputKey: "message",

20 afs,//Agent accesss to all mounted modules});

Listing 2: Attaching a GitHub MCP function.

Report issue for preceding element

VII Conclusion and Future Work
------------------------------

Report issue for preceding element

Grounded in the emerging LLM-as-Operating-System paradigm, this paper presents a file system–based abstraction for context engineering. On this foundation, agents and humans interact as OS-like processes applying standard file operations governed by metadata and transaction logs. The implementation within the AIGNE framework and accompanying exemplars demonstrate the feasibility and adaptability of the proposed approach. Treating context as files further enables GenAI agents to become traceable and auditable, allowing context to be versioned, reviewed, and deployed using DevOps and data-ops practices rather than ad hoc prompt management. By treating the file system as a universal context projection layer, the architecture provides a concrete substrate for emerging LLM-as-OS paradigms, enabling agents to navigate, organize, and evolve their own world models in a verifiable, human-aligned manner.

Report issue for preceding element

Future extensions will explore agentic navigation within the AFS hierarchy, enabling agents to autonomously browse, construct indices, and evolve data structures in the mounted space. By allowing agents to function as self-organising processes that observe and modify their own context, the architecture can gradually evolve into a living knowledge fabric, where reasoning, memory, and action converge within a verifiable and extensible file system substrate. Another important direction is to strengthen human–AI co-work, empowering humans not only to oversee or correct system behaviour but also to contribute to, curate, and contextualise knowledge as active participants in context engineering.

Report issue for preceding element

Report Issue

##### Report Github Issue

Title:Content selection saved. Describe the issue below:Description:

Submit without GithubSubmit in Github

Report Issue for Selection

Generated by [L A T E xml ![[LOGO]](data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAsAAAAOCAYAAAD5YeaVAAAAAXNSR0IArs4c6QAAAAZiS0dEAP8A/wD/oL2nkwAAAAlwSFlzAAALEwAACxMBAJqcGAAAAAd0SU1FB9wKExQZLWTEaOUAAAAddEVYdENvbW1lbnQAQ3JlYXRlZCB3aXRoIFRoZSBHSU1Q72QlbgAAAdpJREFUKM9tkL+L2nAARz9fPZNCKFapUn8kyI0e4iRHSR1Kb8ng0lJw6FYHFwv2LwhOpcWxTjeUunYqOmqd6hEoRDhtDWdA8ApRYsSUCDHNt5ul13vz4w0vWCgUnnEc975arX6ORqN3VqtVZbfbTQC4uEHANM3jSqXymFI6yWazP2KxWAXAL9zCUa1Wy2tXVxheKA9YNoR8Pt+aTqe4FVVVvz05O6MBhqUIBGk8Hn8HAOVy+T+XLJfLS4ZhTiRJgqIoVBRFIoric47jPnmeB1mW/9rr9ZpSSn3Lsmir1fJZlqWlUonKsvwWwD8ymc/nXwVBeLjf7xEKhdBut9Hr9WgmkyGEkJwsy5eHG5vN5g0AKIoCAEgkEkin0wQAfN9/cXPdheu6P33fBwB4ngcAcByHJpPJl+fn54mD3Gg0NrquXxeLRQAAwzAYj8cwTZPwPH9/sVg8PXweDAauqqr2cDjEer1GJBLBZDJBs9mE4zjwfZ85lAGg2+06hmGgXq+j3+/DsixYlgVN03a9Xu8jgCNCyIegIAgx13Vfd7vdu+FweG8YRkjXdWy329+dTgeSJD3ieZ7RNO0VAXAPwDEAO5VKndi2fWrb9jWl9Esul6PZbDY9Go1OZ7PZ9z/lyuD3OozU2wAAAABJRU5ErkJggg==)](https://math.nist.gov/~BMiller/LaTeXML/) 

Instructions for reporting errors
---------------------------------

We are continuing to improve HTML versions of papers, and your feedback helps enhance accessibility and mobile support. To report errors in the HTML that will help us improve conversion and rendering, choose any of the methods listed below:

*   Click the "Report Issue" button.
*   Open a report feedback form via keyboard, use "**Ctrl + ?**".
*   Make a text selection and click the "Report Issue for Selection" button near your cursor.
*   You can use Alt+Y to toggle on and Alt+Shift+Y to toggle off accessible reporting links at each section.

Our team has already identified [the following issues](https://github.com/arXiv/html_feedback/issues). We appreciate your time reviewing and reporting rendering errors we may not have found yet. Your efforts will help us improve the HTML versions for all readers, because disability should not be a barrier to accessing research. Thank you for your continued support in championing open access for all.

Have a free development cycle? Help support accessibility at arXiv! Our collaborators at LaTeXML maintain a [list of packages that need conversion](https://github.com/brucemiller/LaTeXML/wiki/Porting-LaTeX-packages-for-LaTeXML), and welcome [developer contributions](https://github.com/brucemiller/LaTeXML/issues).