/**
 * SRF Conference Insights - Interactive Paper Analysis Application
 * 
 * This JavaScript application provides a comprehensive web interface for browsing,
 * searching, and analyzing scientific papers from superconducting RF conferences.
 * 
 * Author: Ming Liu <mliu@ihep.ac.cn>
 * Project: SRF Conference Insights
 * Institution: Institute of High Energy Physics, Chinese Academy of Sciences
 * 
 * Features:
 * - Real-time paper search and filtering
 * - Dynamic data visualization with statistics
 * - Responsive design for multiple devices
 * - Fallback to mock data when real data is unavailable
 * - Advanced pagination and sorting capabilities
 * 
 * Dependencies:
 * - Bootstrap 5: UI framework and responsive design
 * - Font Awesome: Icon library for enhanced UX
 * - Modern browsers with ES6+ support
 * 
 * Development Log:
 * - v1.0: Basic paper listing and search functionality
 * - v1.1: Added advanced filtering and statistics
 * - v1.2: Enhanced responsive design and error handling
 * - v1.3: Integrated real-time data loading with fallback mechanisms
 * 
 * Usage:
 *   Include this script in an HTML page with proper Bootstrap and
 *   Font Awesome dependencies. Initialize with initPaperApp().
 */

// Main Paper Analysis Application Class
class PaperAnalysisApp {
    /**
     * Initialize the Paper Analysis Application.
     * 
     * Sets up the application state, loads paper data from available sources,
     * and initializes the user interface components.
     */
    constructor() {
        this.papers = [];
        this.filteredPapers = [];
        this.currentPage = 1;
        this.papersPerPage = 10;
        this.init();
    }

    async init() {
        console.log('Initializing application...');
        this.showLoading('Loading paper data...');
        
        try {
            await this.loadData();
            console.log('Data loaded successfully, paper count:', this.papers.length);
            this.renderPapers();
            this.hideLoading();
            console.log('Application initialization complete');
        } catch (error) {
            console.error('Initialization failed:', error);
            this.showError('Data loading failed, please try again later. Error: ' + error.message);
        }
    }

    async loadData() {
        this.showLoading('正在加载论文数据...');
        
        try {
            // 尝试多个可能的路径，优先使用较小的文件
            const possiblePaths = [
                'data/papers-medium.json',     // 中等大小，10篇论文
                'data/papers-simple.json',     // 最小，5篇论文
                './data/papers-medium.json',
                './data/papers-simple.json',
                'data/papers.json',            // 完整数据，最后尝试
                './data/papers.json'
            ];
            
            let data = null;
            let lastError = null;
            let loadedPath = null;
            
            for (const path of possiblePaths) {
                try {
                    console.log('尝试加载路径:', path);
                    const response = await fetch(path);
                    if (response.ok) {
                        data = await response.json();
                        loadedPath = path;
                        console.log('成功加载数据，路径:', path, '论文数量:', data.papers?.length || 0);
                        break;
                    } else {
                        console.log('HTTP错误:', response.status, response.statusText);
                    }
                } catch (error) {
                    lastError = error;
                    console.log('路径失败:', path, error.message);
                }
            }
            
            if (data && data.papers) {
                this.papers = data.papers;
                console.log('数据加载成功，共', this.papers.length, '篇论文，来源:', loadedPath);
                this.hideLoading();
            } else {
                throw lastError || new Error('所有路径都失败了，没有找到有效数据');
            }
        } catch (error) {
            console.warn('无法加载真实数据，使用模拟数据:', error);
            this.papers = this.generateMockData();
            console.log('生成模拟数据，共', this.papers.length, '篇论文');
            this.hideLoading();
        }
        
        this.filteredPapers = [...this.papers];
        this.updateStats();
    }

    generateMockData() {
        const institutions = [
            'Facility for Rare Isotope Beams, Michigan State University',
            'CERN, Geneva, Switzerland', 
            'Fermilab, Batavia, IL, USA',
            'Lawrence Berkeley National Laboratory',
            'INFN - Laboratori Nazionali di Legnaro'
        ];
        
        const topics = [
            'FRIB Operations', 'Accelerator Improvements', 'Superconducting Technology',
            'Beam Dynamics', 'Target Technology', 'Ion Sources', 'RF Systems',
            'Cryogenics', 'Beam Diagnostics', 'Machine Learning Applications'
        ];

        const mockPapers = [];
        for (let i = 1; i <= 86; i++) {
            const topic = topics[Math.floor(Math.random() * topics.length)];
            const institution = institutions[Math.floor(Math.random() * institutions.length)];
            
            mockPapers.push({
                paper_number: i,
                filename: `${String(i).padStart(3, '0')}_${topic.replace(/\s+/g, '_').toUpperCase()}.pdf`,
                title: `${topic}: Advanced Research and Development`,
                authors: this.generateRandomAuthors(),
                affiliations: [institution],
                abstract: `This paper presents comprehensive research on ${topic.toLowerCase()}. The study investigates advanced methodologies and presents significant findings that contribute to the field of heavy ion accelerator technology. Our findings demonstrate improved performance and novel approaches to solving critical challenges in the field.`,
                keywords: this.generateRandomKeywords(topic),
                page_count: Math.floor(Math.random() * 8) + 2,
                file_size_kb: Math.floor(Math.random() * 5000) + 500,
                figures: Math.floor(Math.random() * 15) + 1,
                tables: Math.floor(Math.random() * 5),
                references: Math.floor(Math.random() * 20) + 5,
                sections: this.generateRandomSections()
            });
        }
        return mockPapers;
    }

    generateRandomAuthors() {
        const firstNames = ['John', 'Mary', 'David', 'Sarah', 'Michael', 'Lisa', 'Robert', 'Jennifer'];
        const lastNames = ['Smith', 'Johnson', 'Brown', 'Davis', 'Wilson', 'Miller', 'Taylor', 'Anderson'];
        const count = Math.floor(Math.random() * 4) + 1;
        const authors = [];
        
        for (let i = 0; i < count; i++) {
            const firstName = firstNames[Math.floor(Math.random() * firstNames.length)];
            const lastName = lastNames[Math.floor(Math.random() * lastNames.length)];
            authors.push(`${firstName} ${lastName}`);
        }
        return authors;
    }

    generateRandomKeywords(topic) {
        const baseKeywords = ['accelerator', 'beam', 'physics', 'technology'];
        const topicKeywords = topic.toLowerCase().split(' ');
        return [...baseKeywords, ...topicKeywords].slice(0, 5);
    }

    generateRandomSections() {
        return {
            'Introduction': 'Introduction content',
            'Methodology': 'Methodology content', 
            'Results': 'Results content',
            'Conclusion': 'Conclusion content'
        };
    }

    updateStats() {
        // 更新头部统计数字
        const totalElement = document.getElementById('totalPapers');
        if (totalElement) {
            totalElement.textContent = this.papers.length;
        }
        
        const filteredElement = document.getElementById('filteredCount');
        if (filteredElement) {
            filteredElement.textContent = this.filteredPapers.length;
        }
        
        const uniqueAuthors = new Set();
        const uniqueInstitutions = new Set();
        let totalImages = 0;

        this.papers.forEach(paper => {
            if (paper.authors && Array.isArray(paper.authors)) {
                paper.authors.forEach(author => uniqueAuthors.add(author));
            }
            if (paper.affiliations && Array.isArray(paper.affiliations)) {
                paper.affiliations.forEach(aff => uniqueInstitutions.add(aff));
            }
            // 处理figures字段 - 可能是数组或数字
            if (paper.figures) {
                if (Array.isArray(paper.figures)) {
                    totalImages += paper.figures.length;
                } else if (typeof paper.figures === 'number') {
                    totalImages += paper.figures;
                }
            }
        });

        const institutionCountElement = document.getElementById('institutionCount');
        if (institutionCountElement) {
            institutionCountElement.textContent = uniqueInstitutions.size;
        }
        
        const totalAuthorsElement = document.getElementById('totalAuthors');
        if (totalAuthorsElement) {
            totalAuthorsElement.textContent = uniqueAuthors.size;
        }
        
        // 计算平均作者数
        const avgAuthorsElement = document.getElementById('avgAuthorsPerPaper');
        if (avgAuthorsElement) {
            const avgAuthors = this.papers.length > 0 
                ? (this.papers.reduce((sum, p) => sum + (p.authors?.length || 0), 0) / this.papers.length).toFixed(1)
                : 0;
            avgAuthorsElement.textContent = avgAuthors;
        }
        
        // 计算主题数量
        const topicCountElement = document.getElementById('topicCount');
        if (topicCountElement) {
            const allKeywords = this.papers.flatMap(p => p.keywords || []);
            const uniqueTopics = [...new Set(allKeywords)];
            topicCountElement.textContent = uniqueTopics.length;
        }
        
        // 计算总页数
        const pageCountElement = document.getElementById('pageCount');
        if (pageCountElement) {
            const totalPages = this.papers.reduce((sum, p) => sum + (p.page_count || 0), 0);
            pageCountElement.textContent = totalPages;
        }
        
        // 更新筛选器选项
        this.updateFilterOptions();
    }
    
    updateFilterOptions() {
        const institutionFilter = document.getElementById('institutionFilter');
        const topicFilter = document.getElementById('topicFilter');
        
        if (institutionFilter) {
            const institutions = [...new Set(this.papers.flatMap(p => p.affiliations || []))];
            institutionFilter.innerHTML = '<option value="">所有机构</option>';
            institutions.slice(0, 50).forEach(inst => { // 限制显示前50个机构
                const option = document.createElement('option');
                option.value = inst;
                option.textContent = inst.length > 50 ? inst.substring(0, 50) + '...' : inst;
                institutionFilter.appendChild(option);
            });
        }
        
        if (topicFilter) {
            const topics = [...new Set(this.papers.flatMap(p => p.keywords || []))];
            topicFilter.innerHTML = '<option value="">所有主题</option>';
            topics.slice(0, 30).forEach(topic => { // 限制显示前30个主题
                const option = document.createElement('option');
                option.value = topic;
                option.textContent = topic;
                topicFilter.appendChild(option);
            });
        }
    }
    
    searchPapers() {
        const searchTerm = document.getElementById('searchInput')?.value.toLowerCase() || '';
        
        this.filteredPapers = this.papers.filter(paper => {
            const title = (paper.title || '').toLowerCase();
            const authors = (paper.authors || []).join(' ').toLowerCase();
            const abstract = (paper.abstract || '').toLowerCase();
            const keywords = (paper.keywords || []).join(' ').toLowerCase();
            
            return title.includes(searchTerm) || 
                   authors.includes(searchTerm) || 
                   abstract.includes(searchTerm) ||
                   keywords.includes(searchTerm);
        });
        
        this.applyFilters();
    }
    
    filterPapers() {
        this.applyFilters();
    }
    
    applyFilters() {
        const institutionFilter = document.getElementById('institutionFilter')?.value || '';
        const topicFilter = document.getElementById('topicFilter')?.value || '';
        const searchTerm = document.getElementById('searchInput')?.value.toLowerCase() || '';
        
        this.filteredPapers = this.papers.filter(paper => {
            // 搜索过滤
            const matchesSearch = !searchTerm || 
                (paper.title || '').toLowerCase().includes(searchTerm) ||
                (paper.authors || []).join(' ').toLowerCase().includes(searchTerm) ||
                (paper.abstract || '').toLowerCase().includes(searchTerm) ||
                (paper.keywords || []).join(' ').toLowerCase().includes(searchTerm);
            
            // 机构过滤
            const matchesInstitution = !institutionFilter || 
                (paper.affiliations || []).some(aff => aff.includes(institutionFilter));
            
            // 主题过滤
            const matchesTopic = !topicFilter || 
                (paper.keywords || []).includes(topicFilter);
            
            return matchesSearch && matchesInstitution && matchesTopic;
        });
        
        this.currentPage = 1;
        this.renderPapers();
        this.updateStats();
    }

    renderPapers() {
        const startIndex = (this.currentPage - 1) * this.papersPerPage;
        const endIndex = startIndex + this.papersPerPage;
        const papersToShow = this.filteredPapers.slice(startIndex, endIndex);

        const papersHtml = papersToShow.map(paper => {
            // 安全处理数据
            const authors = paper.authors && paper.authors.length > 0 ? paper.authors.join(', ') : '未知作者';
            const affiliation = paper.affiliations && paper.affiliations.length > 0 ? paper.affiliations[0] : '未知机构';
            const abstract = paper.abstract || '暂无摘要';
            const figureCount = Array.isArray(paper.figures) ? paper.figures.length : (paper.figures || 0);
            const referenceCount = Array.isArray(paper.references) ? paper.references.length : (paper.references || 0);
            const keywords = paper.keywords && Array.isArray(paper.keywords) ? paper.keywords : [];
            
            return `
                <div class="paper-card" onclick="showPaperDetails(${paper.paper_number})">
                    <div class="d-flex justify-content-between align-items-start mb-2">
                        <h5 class="paper-title mb-0">${paper.title}</h5>
                        <span class="badge bg-secondary">#${paper.paper_number}</span>
                    </div>
                    <div class="paper-meta mb-2">
                        <strong>作者:</strong> ${authors}<br>
                        <strong>机构:</strong> ${affiliation}
                    </div>
                    <p class="text-muted mb-2">${abstract.substring(0, 200)}${abstract.length > 200 ? '...' : ''}</p>
                    <div class="d-flex flex-wrap gap-2">
                        <span class="paper-tag">${paper.page_count || 0} 页</span>
                        <span class="paper-tag">${figureCount} 图</span>
                        <span class="paper-tag">${referenceCount} 引用</span>
                        ${keywords.slice(0, 3).map(kw => `<span class="paper-tag keyword">${kw}</span>`).join('')}
                    </div>
                </div>
            `;
        }).join('');

        document.getElementById('papersList').innerHTML = papersHtml;
        this.renderPagination();
        this.updatePaperCount();
    }

    renderPagination() {
        const totalPages = Math.ceil(this.filteredPapers.length / this.papersPerPage);
        const maxVisible = 5;
        
        let pagination = '';
        
        // 上一页
        if (this.currentPage > 1) {
            pagination += `<li class="page-item">
                <a class="page-link" href="#" onclick="app.goToPage(${this.currentPage - 1})">‹</a>
            </li>`;
        }
        
        // 页码
        const startPage = Math.max(1, this.currentPage - Math.floor(maxVisible / 2));
        const endPage = Math.min(totalPages, startPage + maxVisible - 1);
        
        for (let i = startPage; i <= endPage; i++) {
            const active = i === this.currentPage ? 'active' : '';
            pagination += `<li class="page-item ${active}">
                <a class="page-link" href="#" onclick="app.goToPage(${i})">${i}</a>
            </li>`;
        }
        
        // 下一页
        if (this.currentPage < totalPages) {
            pagination += `<li class="page-item">
                <a class="page-link" href="#" onclick="app.goToPage(${this.currentPage + 1})">›</a>
            </li>`;
        }
        
        document.getElementById('pagination').innerHTML = pagination;
    }

    goToPage(page) {
        this.currentPage = page;
        this.renderPapers();
        window.scrollTo({top: 0, behavior: 'smooth'});
    }

    updatePaperCount() {
        document.getElementById('paperCount').textContent = `${this.filteredPapers.length} 篇论文`;
    }

    hideLoading() {
        const loadingIndicator = document.getElementById('loadingIndicator');
        if (loadingIndicator) {
            loadingIndicator.style.display = 'none';
        }
        const papersList = document.getElementById('papersList');
        if (papersList) {
            papersList.style.display = 'block';
        }
    }

    showLoading(message = '正在加载...') {
        const loadingIndicator = document.getElementById('loadingIndicator');
        if (loadingIndicator) {
            loadingIndicator.style.display = 'block';
            loadingIndicator.innerHTML = `
                <div class="text-center">
                    <i class="fas fa-spinner fa-spin fa-2x text-primary"></i>
                    <p class="mt-3">${message}</p>
                </div>
            `;
        }
        const papersList = document.getElementById('papersList');
        if (papersList) {
            papersList.style.display = 'none';
        }
    }

    showError(message) {
        const loadingIndicator = document.getElementById('loadingIndicator');
        if (loadingIndicator) {
            loadingIndicator.style.display = 'block';
            loadingIndicator.innerHTML = `
                <div class="text-center">
                    <i class="fas fa-exclamation-triangle fa-2x text-danger"></i>
                    <p class="text-danger mt-3">${message}</p>
                    <p class="text-muted">正在使用模拟数据...</p>
                    <button class="btn btn-primary mt-2" onclick="location.reload()">重试</button>
                </div>
            `;
        }
    }

    // 搜索功能
    searchPapers(query) {
        if (!query) {
            this.filteredPapers = [...this.papers];
        } else {
            query = query.toLowerCase();
            this.filteredPapers = this.papers.filter(paper => {
                // 安全检查每个字段
                const title = (paper.title || '').toLowerCase();
                const abstract = (paper.abstract || '').toLowerCase();
                const authors = Array.isArray(paper.authors) ? paper.authors.join(' ').toLowerCase() : '';
                const affiliations = Array.isArray(paper.affiliations) ? paper.affiliations.join(' ').toLowerCase() : '';
                const keywords = Array.isArray(paper.keywords) ? paper.keywords.join(' ').toLowerCase() : '';
                
                return title.includes(query) ||
                       abstract.includes(query) ||
                       authors.includes(query) ||
                       affiliations.includes(query) ||
                       keywords.includes(query);
            });
        }
        
        this.currentPage = 1;
        this.renderPapers();
    }

    // 排序功能
    sortPapers(sortBy) {
        this.filteredPapers.sort((a, b) => {
            switch (sortBy) {
                case 'title':
                    return (a.title || '').localeCompare(b.title || '');
                case 'pages':
                    return (b.page_count || 0) - (a.page_count || 0);
                case 'figures':
                    const aFigures = Array.isArray(a.figures) ? a.figures.length : (a.figures || 0);
                    const bFigures = Array.isArray(b.figures) ? b.figures.length : (b.figures || 0);
                    return bFigures - aFigures;
                case 'number':
                default:
                    return (a.paper_number || 0) - (b.paper_number || 0);
            }
        });
        
        this.currentPage = 1;
        this.renderPapers();
    }

    // 过滤功能
    filterByInstitution(institution) {
        this.filteredPapers = this.papers.filter(paper => 
            paper.affiliations.some(aff => aff.toLowerCase().includes(institution.toLowerCase()))
        );
        this.currentPage = 1;
        this.renderPapers();
    }

    filterByContent(keyword) {
        this.filteredPapers = this.papers.filter(paper => 
            paper.title.toLowerCase().includes(keyword.toLowerCase()) ||
            paper.abstract.toLowerCase().includes(keyword.toLowerCase()) ||
            paper.keywords.some(kw => kw.toLowerCase().includes(keyword.toLowerCase()))
        );
        this.currentPage = 1;
        this.renderPapers();
    }

    clearFilters() {
        this.filteredPapers = [...this.papers];
        this.currentPage = 1;
        this.renderPapers();
        document.getElementById('searchInput').value = '';
    }
}

// 全局函数
function searchPapers() {
    const query = document.getElementById('searchInput').value;
    app.searchPapers(query);
}

function sortPapers() {
    const sortBy = document.getElementById('sortSelect').value;
    app.sortPapers(sortBy);
}

function filterByInstitution(institution) {
    app.filterByInstitution(institution);
}

function filterByContent(content) {
    app.filterByContent(content);
}

function clearFilters() {
    app.clearFilters();
}

function showPaperDetails(paperNumber) {
    const paper = app.papers.find(p => p.paper_number === paperNumber);
    if (!paper) return;
    
    // 安全处理数据
    const authors = paper.authors && paper.authors.length > 0 ? paper.authors.join(', ') : '未知作者';
    const affiliations = paper.affiliations && paper.affiliations.length > 0 ? paper.affiliations.join('; ') : '未知机构';
    const abstract = paper.abstract || '暂无摘要信息';
    const keywords = paper.keywords && Array.isArray(paper.keywords) ? paper.keywords : [];
    const figureCount = Array.isArray(paper.figures) ? paper.figures.length : (paper.figures || 0);
    const tableCount = Array.isArray(paper.tables) ? paper.tables.length : (paper.tables || 0);
    const referenceCount = Array.isArray(paper.references) ? paper.references.length : (paper.references || 0);
    
    document.getElementById('modalTitle').textContent = paper.title;
    document.getElementById('modalBody').innerHTML = `
        <div class="row mb-3">
            <div class="col-md-6">
                <strong>作者:</strong> ${authors}<br>
                <strong>机构:</strong> ${affiliations}<br>
                <strong>页数:</strong> ${paper.page_count || 0} 页
            </div>
            <div class="col-md-6">
                <strong>图片:</strong> ${figureCount} 张<br>
                <strong>表格:</strong> ${tableCount} 个<br>
                <strong>参考文献:</strong> ${referenceCount} 条
            </div>
        </div>
        
        ${keywords.length > 0 ? `
        <div class="mb-3">
            <strong>关键词:</strong><br>
            <div class="mt-1">
                ${keywords.map(kw => `<span class="paper-tag keyword">${kw}</span>`).join('')}
            </div>
        </div>
        ` : ''}
        
        <div class="mb-3">
            <strong>摘要:</strong><br>
            <p class="text-muted mt-2">${abstract}</p>
        </div>
        
        <div class="mb-3">
            <strong>文件信息:</strong><br>
            <small class="text-muted">
                文件名: ${paper.filename || '未知'}<br>
                文件大小: ${paper.file_size_kb ? `${paper.file_size_kb.toFixed(2)} KB` : '未知'}
            </small>
        </div>
    `;
    
    const modal = new bootstrap.Modal(document.getElementById('paperModal'));
    modal.show();
}

// 初始化应用
document.addEventListener('DOMContentLoaded', () => {
    // 不在这里自动初始化，而是在标签页切换时初始化
    
    // 搜索事件监听
    const searchInput = document.getElementById('searchInput');
    if (searchInput) {
        searchInput.addEventListener('keyup', (e) => {
            if (window.app && window.app.searchPapers) {
                window.app.searchPapers();
            }
        });
        
        searchInput.addEventListener('input', () => {
            if (window.app && window.app.searchPapers) {
                window.app.searchPapers();
            }
        });
    }
    
    // 筛选器事件监听
    const institutionFilter = document.getElementById('institutionFilter');
    const topicFilter = document.getElementById('topicFilter');
    
    if (institutionFilter) {
        institutionFilter.addEventListener('change', () => {
            if (window.app && window.app.filterPapers) {
                window.app.filterPapers();
            }
        });
    }
    
    if (topicFilter) {
        topicFilter.addEventListener('change', () => {
            if (window.app && window.app.filterPapers) {
                window.app.filterPapers();
            }
        });
    }
});

// 全局函数用于标签页初始化论文应用
function initPaperApp() {
    if (!window.app) {
        window.app = new PaperAnalysisApp();
    }
}
