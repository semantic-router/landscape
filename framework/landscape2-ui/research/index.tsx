import { useLocation, useNavigate } from '@solidjs/router';
import { Loading, NoData, SVGIcon, SVGIconKind, useBreakpointDetect } from 'common';
import isUndefined from 'lodash/isUndefined';
import { createEffect, createSignal, For, Match, on, onMount, Show, Switch } from 'solid-js';

import { RESEARCH_PATH, SMALL_DEVICES_BREAKPOINTS } from '../../data';
import { CategoryGuide, Guide, SubcategoryGuide, ToCTitle } from '../../types';
import goToElement from '../../utils/goToElement';
import isElementInView from '../../utils/isElementInView';
import buildNormalizedId from '../../utils/normalizeId';
import scrollToTop from '../../utils/scrollToTop';
import ButtonToTopScroll from '../common/ButtonToTopScroll';
import { Sidebar } from '../common/Sidebar';
import Footer from '../navigation/Footer';
import { useMobileTOCStatus, useSetMobileTOCStatus } from '../stores/mobileTOC';
import styles from '../guide/Guide.module.css';
import ToC from '../guide/ToC';

type ResearchLoadStatus = 'error' | 'loading' | 'ready';

const getResearchUrl = () =>
  import.meta.env.MODE === 'development' ? '../../static/data/research-guide.json' : './data/research-guide.json';

const ResearchIndex = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const [research, setResearch] = createSignal<Guide>();
  const [loadStatus, setLoadStatus] = createSignal<ResearchLoadStatus>('loading');
  const [toc, setToc] = createSignal<ToCTitle[]>([]);
  const [firstItem, setFirstItem] = createSignal<string>();
  const [openToCMobileStatus, setOpenToCMobileStatus] = createSignal<boolean>(false);
  const openMenuTOCFromHeader = useMobileTOCStatus();
  const setMenuTOCFromHeader = useSetMobileTOCStatus();
  const { point } = useBreakpointDetect();
  const onSmallDevice = !isUndefined(point()) && SMALL_DEVICES_BREAKPOINTS.includes(point()!);

  const prepareToC = (data: Guide) => {
    const content: ToCTitle[] = [];
    data.categories.forEach((category: CategoryGuide) => {
      const subcategories: ToCTitle[] = [];
      category.subcategories?.forEach((subcategory: SubcategoryGuide) => {
        subcategories.push({
          title: subcategory.subcategory,
          id: buildNormalizedId({
            title: category.category,
            subtitle: subcategory.subcategory,
            grouped: true,
          }),
        });
      });
      content.push({
        title: category.category,
        id: buildNormalizedId({ title: category.category }),
        options: subcategories,
      });
    });

    if (content.length > 0) setFirstItem(content[0].id);
    setToc(content);
  };

  const fetchResearch = async () => {
    setLoadStatus('loading');
    try {
      const response = await fetch(getResearchUrl());
      if (!response.ok) throw new Error(`Unable to load research: ${response.status}`);
      const data = (await response.json()) as Guide;
      setResearch(data);
      prepareToC(data);
      setLoadStatus('ready');
    } catch {
      setResearch(undefined);
      setLoadStatus('error');
    }
  };

  const updateRoute = (title: string) => {
    navigate(`${RESEARCH_PATH}${location.search}#${title}`, {
      replace: true,
      scroll: false,
      state: { fromMenu: true },
    });
  };

  const openStatusChange = (open: boolean) => {
    setOpenToCMobileStatus(open);
    setMenuTOCFromHeader(open);
  };

  const updateActiveTitle = (title: string, onLoad?: boolean) => {
    updateRoute(title);
    if (onSmallDevice) openStatusChange(false);
    if (title === firstItem()) {
      scrollToTop(onSmallDevice);
    } else if (onLoad) {
      setTimeout(() => goToElement(`section_${title}`), 50);
    } else {
      goToElement(`section_${title}`);
    }
  };

  const scrollInToC = () => {
    const cleanHash = location.hash.replace('#', '');
    if (!isElementInView(`btn_${cleanHash}`)) {
      window.document.getElementById(`btn_${cleanHash}`)?.scrollIntoView({ block: 'nearest' });
    }
  };

  onMount(() => void fetchResearch());

  createEffect(
    on(toc, () => {
      if (toc().length === 0 || !firstItem()) return;
      const cleanHash = location.hash.replace('#', '');
      if (cleanHash !== '' && cleanHash !== firstItem()) {
        setTimeout(() => {
          updateActiveTitle(cleanHash, true);
          scrollInToC();
        }, 25);
      } else {
        updateRoute(firstItem()!);
      }
    })
  );

  createEffect(on(openMenuTOCFromHeader, () => setOpenToCMobileStatus(openMenuTOCFromHeader())));

  return (
    <>
      <main class="flex-grow-1 container-fluid px-3 px-lg-4 mainPadding position-relative">
        <Show when={loadStatus() === 'ready'}>
          <div class="d-block d-lg-none">
            <Sidebar
              label="Index"
              header="Index"
              visibleButton
              buttonIcon={<SVGIcon kind={SVGIconKind.ToC} />}
              buttonType={`position-relative btn btn-sm btn-secondary text-white btn-sm rounded-0 py-0 mt-3 btnIconMobile ${styles.mobileToCBtn}`}
              open={openToCMobileStatus()}
              onOpenStatusChange={openStatusChange}
            >
              <div class="position-relative">
                <ToC toc={toc()} updateActiveTitle={updateActiveTitle} sticky={false} />
              </div>
            </Sidebar>
          </div>
        </Show>
        <div class="d-flex flex-row" classList={{ [styles.loadingContent]: loadStatus() === 'loading' }}>
          <Switch>
            <Match when={loadStatus() === 'loading'}>
              <Loading spinnerClass="position-fixed top-50 start-50" />
            </Match>
            <Match when={loadStatus() === 'error'}>
              <div class="w-100 py-5">
                <NoData>
                  <div class="d-flex flex-column align-items-center">
                    <div class="fs-5">We couldn't load the research index.</div>
                    <button type="button" class="btn btn-secondary mt-3" onClick={() => void fetchResearch()}>
                      Try again
                    </button>
                  </div>
                </NoData>
              </div>
            </Match>
            <Match when={loadStatus() === 'ready'}>
              <div class="d-none d-lg-flex">
                <ToC toc={toc()} updateActiveTitle={updateActiveTitle} sticky />
              </div>
              <div class="py-3 px-0 p-lg-4 pe-lg-0">
                <div class={`position-relative ${styles.guide}`}>
                  <For each={research()!.categories}>
                    {(category, categoryIndex) => {
                      const id = buildNormalizedId({ title: category.category });
                      const hasSubcategories = !isUndefined(category.subcategories) && category.subcategories.length > 0;
                      return (
                        <>
                          <div
                            id={`section_${id}`}
                            class={styles.section}
                            classList={{ [styles.catSection]: !hasSubcategories }}
                          >
                            <h1
                              class={`border-bottom mb-3 mb-lg-4 pb-2 ${styles.title}`}
                              classList={{ 'mt-4 mt-lg-5': categoryIndex() !== 0 }}
                            >
                              {category.category}
                            </h1>
                            <Show when={!isUndefined(category.content)}>
                              <div innerHTML={category.content} />
                            </Show>
                          </div>
                          <Show when={hasSubcategories}>
                            <For each={category.subcategories}>
                              {(subcategory, subcategoryIndex) => {
                                const subcategoryId = buildNormalizedId({
                                  title: category.category,
                                  subtitle: subcategory.subcategory,
                                  grouped: true,
                                });
                                return (
                                  <div
                                    id={`section_${subcategoryId}`}
                                    class={styles.section}
                                    classList={{
                                      [styles.catSection]: subcategoryIndex() === category.subcategories.length - 1,
                                    }}
                                  >
                                    <h2 class={`mt-4 mt-lg-5 mb-3 mb-lg-4 pb-2 border-bottom ${styles.subtitle}`}>
                                      {subcategory.subcategory}
                                    </h2>
                                    <div innerHTML={subcategory.content} />
                                  </div>
                                );
                              }}
                            </For>
                          </Show>
                        </>
                      );
                    }}
                  </For>
                </div>
              </div>
            </Match>
          </Switch>
        </div>
        <Show when={loadStatus() === 'ready'}>
          <ButtonToTopScroll />
        </Show>
      </main>
      <Show when={loadStatus() === 'ready'}>
        <Footer />
      </Show>
    </>
  );
};

export default ResearchIndex;
