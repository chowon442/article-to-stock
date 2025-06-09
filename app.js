// API 응답 데이터를 저장할 전역 변수
let apiResponseData = null;

// DOM 요소들
const urlInput = document.getElementById('url-input');
const analyzeBtn = document.getElementById('analyze-btn');
const resetBtn = document.getElementById('reset-btn');
const loadingSection = document.getElementById('loading-section');
const resultsSection = document.getElementById('results-section');
const resultsGrid = document.getElementById('results-grid');
const articleContent = document.getElementById('article-content');
const skeletonArticle = document.getElementById('skeleton-article');
const loadingGridSkeletons = document.getElementById('loading-grid-skeletons');
const notNewsSection = document.getElementById('not-news-section');

// HTML 태그 제거 함수
function stripHtmlTags(str) {
    if (!str) return '';
    return str.replace(/<[^>]*>/g, '').replace(/&nbsp;/g, ' ').trim();
}

// 스켈레톤 카드 HTML 생성 함수
function createSkeletonCardHtml() {
    return `
        <div class="skeleton-card">
            <div class="skeleton-header"></div>
            <div class="skeleton-content">
                <div class="skeleton-line"></div>
                <div class="skeleton-line short"></div>
            </div>
        </div>
    `;
}

// 스켈레톤 카드 동적 생성 및 표시 함수
function displaySkeletonCards(count) {
    if (!loadingGridSkeletons) return; // 요소가 없으면 종료

    loadingGridSkeletons.innerHTML = ''; // 기존 스켈레톤 제거
    for (let i = 0; i < count; i++) {
        loadingGridSkeletons.insertAdjacentHTML('beforeend', createSkeletonCardHtml());
    }
}

// 상태 관리
let isAnalyzing = false;

// 이벤트 리스너 등록
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM Content Loaded.');
    analyzeBtn.addEventListener('click', handleAnalyze);
    resetBtn.addEventListener('click', handleReset);
    
    // Enter 키로 분석 시작
    urlInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter' && !isAnalyzing) {
            handleAnalyze();
        }
    });
});

// 분석 시작 함수
function handleAnalyze() {
    const url = urlInput.value.trim();
    
    // URL 유효성 검사
    if (!url) {
        alert('분석할 링크 주소를 입력해주세요.');
        urlInput.focus();
        return;
    }
    
    if (!isValidUrl(url)) {
        alert('올바른 URL 형식을 입력해주세요.');
        urlInput.focus();
        return;
    }
    
    startAnalysis();
}

// URL 유효성 검사
function isValidUrl(string) {
    try {
        new URL(string);
        return true;
    } catch (_) {
        return false;
    }
}

// 분석 시작
function startAnalysis() {
    isAnalyzing = true;
    
    // 버튼 상태 변경
    analyzeBtn.disabled = true;
    analyzeBtn.textContent = '분석 중...';
    
    // 입력 필드 비활성화
    urlInput.disabled = true;
    
    // 기존 결과 숨김
    hideResults();
    
    // 기사 내용 영역 숨김
    articleContent.classList.add('hidden');
    
    // 뉴스 기사가 아닌 경우 섹션 숨김
    if (notNewsSection) {
        notNewsSection.classList.add('hidden');
    }

    // 로딩 UI 표시
    showLoading();

    // 스켈레톤 카드 동적 생성 및 표시
    displaySkeletonCards(6); // 적절한 개수로 조정
    
    // 기사 내용 가져오기
    fetchArticleContent(urlInput.value);
}

// 기사 내용 가져오기
async function fetchArticleContent(url) {
    try {
        const response = await fetch('/api/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ url: url }),
        });
        
        const data = await response.json();
        console.log('API Response:', data);
        
        if (data.status === 'success' && data.result) {
            // 성공적으로 분석된 경우
            apiResponseData = data.result;
            
            // is_news_article 확인
            if (apiResponseData.is_news_article === false) {
                // 뉴스 기사가 아닌 경우
                setTimeout(() => {
                    hideLoading();
                    showNotNewsMessage();
                    finishAnalysis();
                }, 1000);
            } else {
                // 뉴스 기사인 경우
                // 기사 내용 표시
                if (apiResponseData.article) {
                    displayArticleContent(url, apiResponseData.article);
                }
                
                // 결과 표시
                setTimeout(() => {
                    hideLoading();
                    showResults();
                    finishAnalysis();
                }, 1000);
            }
            
        } else {
            // 분석 실패한 경우
            console.error('분석 실패:', data.message || '알 수 없는 오류');
            handleAnalysisError(data.message || '분석에 실패했습니다.');
        }
        
    } catch (error) {
        console.error('API 호출 중 오류가 발생했습니다:', error);
        handleAnalysisError('서버와의 통신 중 오류가 발생했습니다.');
    }
}

// 분석 오류 처리
function handleAnalysisError(message) {
    hideLoading();
    alert(message);
    finishAnalysis();
}

// 기사 내용 표시
function displayArticleContent(url, article) {
    const articleContent = document.getElementById('article-content');
    const articleTitle = document.getElementById('article-content').querySelector('.article-content__title');
    const articleUrl = document.getElementById('article-url');
    const articleText = document.getElementById('article-text');
    
    if (articleTitle) {
        articleTitle.textContent = article.title || '제목 없음';
    }

    articleUrl.textContent = url;
    const cleanContent = stripHtmlTags(article.content || '');
    articleText.innerHTML = '';
    
    // 기사 내용 추가
    const contentElement = document.createElement('div');
    contentElement.textContent = cleanContent || '내용 없음';
    contentElement.style.lineHeight = '1.6';
    articleText.appendChild(contentElement);
    
    // 기사 내용 영역 표시
    articleContent.classList.remove('hidden');
}

// 로딩 UI 표시
function showLoading() {
    loadingSection.classList.remove('hidden');
    loadingSection.classList.add('fade-in');
    
    // 기사 스켈레톤 표시
    if (skeletonArticle) {
        skeletonArticle.classList.remove('hidden');
    }
}

// 로딩 UI 숨김
function hideLoading() {
    loadingSection.classList.add('hidden');
    loadingSection.classList.remove('fade-in');
    
    // 기사 스켈레톤 숨김
    if (skeletonArticle) {
        skeletonArticle.classList.add('hidden');
    }
}

// 결과 표시
function showResults() {
    // 결과 카드들 생성
    createResultCards();
    
    // 결과 섹션 표시
    resultsSection.classList.remove('hidden');
    resultsSection.classList.add('fade-in');
    
    // 초기화 버튼 표시
    resetBtn.classList.remove('hidden');
}

// 결과 카드 생성
function createResultCards() {
    // 기존 카드들 제거
    resultsGrid.innerHTML = '';
    
    // API 응답 데이터가 있고 회사 정보가 있는 경우
    if (apiResponseData && apiResponseData.companies && apiResponseData.companies.length > 0) {
        apiResponseData.companies.forEach((company, index) => {
            const card = createCompanyCard(company, index);
            resultsGrid.appendChild(card);
        });
    } else {
        // 회사 정보가 없는 경우 메시지 표시
        const noDataMessage = document.createElement('div');
        noDataMessage.className = 'no-companies-message';
        noDataMessage.innerHTML = `
            <div style="text-align: center; padding: 40px; color: #666;">
                <h3 style="margin-bottom: 10px;">분석된 기업 정보가 없습니다</h3>
                <p>이 기사에서는 주식 관련 기업 정보를 찾을 수 없습니다.</p>
            </div>
        `;
        resultsGrid.appendChild(noDataMessage);
    }
}

// 개별 회사 카드 생성
function createCompanyCard(company, index) {
    const card = document.createElement('div');
    card.className = 'company-card';
    
    // 새로운 형식 데이터 사용
    const companyName = company.name || '회사명 없음';
    const companyCode = company.code ? `(${company.code})` : '';
    const impact = company.impact || '정보 없음';
    const comment = company.comment || '설명 없음';
    const changes = company.changes || '변동률 없음';
    const finalPrice = company.final_price ? `현재가: ${company.final_price.toLocaleString()}원` : '';
    
    // 영향도에 따른 클래스 결정
    let impactClass = 'neutral';
    if (impact.includes('긍정')) {
        impactClass = 'positive';
    } else if (impact.includes('부정')) {
        impactClass = 'negative';
    }
    
    // 변동률에 따른 클래스 결정
    let percentageClass = 'neutral';
    if (changes.startsWith('+') || changes.startsWith('▲')) {
        percentageClass = 'positive';
    } else if (changes.startsWith('-') || changes.startsWith('▼')) {
        percentageClass = 'negative';
    }
    
    card.innerHTML = `
        <div class="company-card__header">
            <h3 class="company-card__name">${companyName} ${companyCode}</h3>
            <span class="company-card__impact company-card__impact--${impactClass}">
                ${impact}
            </span>
        </div>
        <p class="company-card__description">${comment}</p>
        ${finalPrice ? `<div class="company-card__price">${finalPrice}</div>` : ''}
        <div class="company-card__percentage company-card__percentage--${percentageClass}">
            ${changes}
        </div>
    `;
    
    return card;
}

// 뉴스 기사가 아닌 경우 메시지 표시
function showNotNewsMessage() {
    if (notNewsSection) {
        notNewsSection.classList.remove('hidden');
        notNewsSection.classList.add('fade-in');
    }
    
    // 초기화 버튼 표시
    resetBtn.classList.remove('hidden');
}

// 뉴스 기사가 아닌 경우 메시지 숨김
function hideNotNewsMessage() {
    if (notNewsSection) {
        notNewsSection.classList.add('hidden');
        notNewsSection.classList.remove('fade-in');
    }
}

// 결과 숨김
function hideResults() {
    resultsSection.classList.add('hidden');
    resultsSection.classList.remove('fade-in');
    resetBtn.classList.add('hidden');
}

// 분석 완료
function finishAnalysis() {
    isAnalyzing = false;
    
    // 버튼 상태 복원
    analyzeBtn.disabled = false;
    analyzeBtn.textContent = '분석 시작';
    
    // 입력 필드 활성화
    urlInput.disabled = false;
}

// 초기화 처리
function handleReset() {
    // API 응답 데이터 초기화
    apiResponseData = null;
    
    hideResults();
    hideLoading();
    hideNotNewsMessage();
    
    // 입력 필드 초기화
    urlInput.value = '';
    urlInput.disabled = false;
    urlInput.focus();
    
    // 기사 내용 초기화
    document.getElementById('article-content').classList.add('hidden');
    const articleTitle = document.getElementById('article-content').querySelector('.article-content__title');
    if (articleTitle) {
        articleTitle.textContent = '기사 내용';
    }
    document.getElementById('article-url').textContent = '';
    document.getElementById('article-text').textContent = '';
    
    // 버튼 상태 초기화
    analyzeBtn.disabled = false;
    analyzeBtn.textContent = '분석 시작';
    resetBtn.classList.add('hidden');
}

// 페이지 로드 시 입력 필드에 포커스
window.addEventListener('load', function() {
    urlInput.focus();
});