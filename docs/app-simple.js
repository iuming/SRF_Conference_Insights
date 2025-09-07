// HIAT2025 简化版论文分析系统
class PaperAnalysisApp {
    constructor() {
        this.papers = [];
        this.filteredPapers = [];
        this.currentPage = 1;
        this.papersPerPage = 10;
        this.init();
    }

    async init() {
        try {
            await this.loadData();
            this.renderPapers();
            this.hideLoading();
        } catch (error) {
            console.error('初始化失败:', error);
            this.showError('数据加载失败，请稍后重试');
        }
    }

    async loadData() {
        try {
            const response = await fetch('data/papers.json');
            if (!response.ok) {
                throw new Error('数据文件不存在');
            }
            const data = await response.json();
            this.papers = data.papers || [];
        } catch (error) {
            console.warn('使用模拟数据:', error);
            this.papers = this.generateMockData();
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
        document.getElementById('total-papers').textContent = this.papers.length;
        
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

        document.getElementById('total-authors').textContent = uniqueAuthors.size;
        document.getElementById('total-institutions').textContent = uniqueInstitutions.size;
        document.getElementById('total-images').textContent = totalImages;
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
        document.getElementById('loadingIndicator').style.display = 'none';
        document.getElementById('papersList').style.display = 'block';
    }

    showError(message) {
        document.getElementById('loadingIndicator').innerHTML = `
            <i class="fas fa-exclamation-triangle fa-2x text-danger"></i>
            <p class="text-danger">${message}</p>
            <p class="text-muted">正在使用模拟数据...</p>
        `;
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
    window.app = new PaperAnalysisApp();
    
    // 搜索事件监听
    document.getElementById('searchInput').addEventListener('keyup', (e) => {
        if (e.key === 'Enter') {
            searchPapers();
        }
    });
    
    // 排序事件监听
    document.getElementById('sortSelect').addEventListener('change', sortPapers);
});
