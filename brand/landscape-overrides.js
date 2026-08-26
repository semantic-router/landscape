(() => {
  const FULL_GROUP_NAME = "Everything";
  const FULL_GROUP_VALUE = "everything";
  const categories = [
    "Open Routing Systems",
    "Routing Products",
    "Evaluation and Community",
    "Gateway and Execution",
  ];

  const categoryRank = (value = "") => {
    const normalized = value.toLowerCase().replace(/[^a-z]+/g, " ").trim();
    if (normalized.includes("open routing systems")) return 0;
    if (normalized.includes("routing products")) return 1;
    if (normalized.includes("evaluation and community")) return 2;
    if (normalized.includes("gateway and execution")) return 3;
    return Number.POSITIVE_INFINITY;
  };

  const stableReorder = (elements, getRank) => {
    if (elements.length < 2) return;
    const parent = elements[0].parentElement;
    if (!parent || elements.some((element) => element.parentElement !== parent)) return;

    const sorted = elements
      .map((element, index) => ({ element, index, rank: getRank(element) }))
      .sort((a, b) => a.rank - b.rank || a.index - b.index);

    if (sorted.every(({ element }, index) => element === elements[index])) return;
    sorted.forEach(({ element }) => parent.append(element));
  };

  const reorderCardSections = () => {
    const categoryContainers = [
      ...new Set(
        [...document.querySelectorAll('[id^="card_"]')]
          .map((section) => section.parentElement)
          .filter(Boolean),
      ),
    ];
    const containersByParent = new Map();

    categoryContainers.forEach((container) => {
      const parent = container.parentElement;
      if (!parent) return;
      if (!containersByParent.has(parent)) containersByParent.set(parent, []);
      containersByParent.get(parent).push(container);
    });

    containersByParent.forEach((containers) => {
      stableReorder(containers, (container) => {
        const firstSection = container.querySelector('[id^="card_"]');
        return categoryRank(firstSection?.id || "");
      });
    });
  };

  const reorderCategoryNavigation = () => {
    const labels = [...document.querySelectorAll("div")].filter((element) =>
      categories.includes(element.textContent.trim()),
    );

    const wrappersByParent = new Map();
    labels.forEach((label) => {
      const wrapper = label.parentElement;
      const parent = wrapper?.parentElement;
      if (!wrapper || !parent) return;
      if (!wrappersByParent.has(parent)) wrappersByParent.set(parent, []);
      wrappersByParent.get(parent).push(wrapper);
    });

    wrappersByParent.forEach((wrappers) => {
      if (new Set(wrappers).size < 2) return;
      stableReorder([...new Set(wrappers)], (wrapper) => categoryRank(wrapper.textContent));
    });
  };

  const pinVllmSemanticRouter = () => {
    document.querySelectorAll('img[alt="vLLM Semantic Router logo"]').forEach((img) => {
      const card = img.closest(".card");
      const column = card?.parentElement;
      const row = column?.parentElement;
      if (row?.classList.contains("row") && row.firstElementChild !== column) {
        row.prepend(column);
      }
    });
  };

  const labelFullGroupAsAll = () => {
    document.querySelectorAll(`button[title="Group: ${FULL_GROUP_NAME}"]`).forEach((button) => {
      button.title = "Group: All";
      button.setAttribute("aria-label", "All");
      if (button.textContent.trim() !== "All") button.textContent = "All";
    });

    document.querySelectorAll(`select option[value="${FULL_GROUP_VALUE}"]`).forEach((option) => {
      if (option.textContent.trim() !== "All") option.textContent = "All";
    });
  };

  let gridZoomInitialized = false;

  const initializeGridZoom = () => {
    const gridButton = document.querySelector('button[title="View mode: Grid"]');
    const gridIsActive = gridButton?.classList.contains("active");

    if (!gridIsActive) {
      gridZoomInitialized = false;
      return;
    }
    if (gridZoomInitialized) return;

    const grid = [...document.querySelectorAll('[class*="zoom-"]')].find(
      (element) => element.offsetParent !== null,
    );
    const zoomLevel = [...(grid?.classList || [])]
      .map((className) => className.match(/^zoom-(\d+)$/)?.[1])
      .find(Boolean);

    if (zoomLevel === "10") {
      gridZoomInitialized = true;
      return;
    }

    const increase = document.querySelector('button[aria-label="Increase zoom level"]');
    if (increase && !increase.disabled) {
      increase.click();
      requestAnimationFrame(initializeGridZoom);
    }
  };

  let scrollFrame;
  let observedLandscape;

  const syncCardTabToScroll = () => {
    scrollFrame = undefined;

    const cardButton = document.querySelector('button[title="View mode: Card"]');
    if (!cardButton?.classList.contains("active")) return;

    const landscape = document.getElementById("landscape");
    if (!landscape) return;

    const sections = [...document.querySelectorAll('[id^="card_"]')]
      .filter((section) => section.offsetParent !== null)
      .sort((a, b) => a.getBoundingClientRect().top - b.getBoundingClientRect().top);
    if (!sections.length) return;

    const landscapeTop = landscape.getBoundingClientRect().top;
    const activationLine = landscapeTop + Math.min(180, landscape.clientHeight * 0.28);
    const activeSection =
      [...sections].reverse().find((section) => section.getBoundingClientRect().top <= activationLine) || sections[0];
    const hash = activeSection.id.replace(/^card_/, "");
    if (!hash || window.location.hash === `#${hash}`) return;

    const nextUrl = `${window.location.pathname}${window.location.search}#${hash}`;
    window.history.replaceState(window.history.state, "", nextUrl);
    window.dispatchEvent(new PopStateEvent("popstate", { state: window.history.state }));
  };

  const queueScrollSync = () => {
    if (scrollFrame) return;
    scrollFrame = requestAnimationFrame(syncCardTabToScroll);
  };

  const attachCardScrollSync = () => {
    const landscape = document.getElementById("landscape");
    if (!landscape || landscape === observedLandscape) return;

    observedLandscape?.removeEventListener("scroll", queueScrollSync);
    observedLandscape = landscape;
    observedLandscape.addEventListener("scroll", queueScrollSync, { passive: true });
  };

  const refine = () => {
    labelFullGroupAsAll();
    reorderCardSections();
    reorderCategoryNavigation();
    pinVllmSemanticRouter();
    attachCardScrollSync();
    initializeGridZoom();
    queueScrollSync();
  };

  const start = () => {
    let queued = false;
    const queue = () => {
      if (queued) return;
      queued = true;
      requestAnimationFrame(() => {
        queued = false;
        refine();
      });
    };

    new MutationObserver(queue).observe(document.body, { childList: true, subtree: true });
    window.addEventListener("popstate", queue);
    queue();
  };

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", start, { once: true });
  } else {
    start();
  }
})();
