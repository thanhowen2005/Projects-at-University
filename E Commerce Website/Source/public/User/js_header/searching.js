// Chức năng tìm kiếm sản phẩm với dropdown suggestion
class ProductSearch {
    constructor() {
        this.searchInput = document.querySelector('.search_input');
        this.searchContainer = document.querySelector('.search');
        this.suggestionsContainer = null;
        this.debounceTimer = null;
        this.selectedIndex = -1;
        this.suggestions = [];
        this.init();
    }

    init() {
        if (!this.searchInput || !this.searchContainer) {
            console.warn('Search elements not found');
            return;
        }

        this.createSuggestionsContainer();
        this.attachEventListeners();
    }

    createSuggestionsContainer() {
        // Tạo container cho dropdown suggestions
        this.suggestionsContainer = document.createElement('div');
        this.suggestionsContainer.className = 'search-suggestions';
        
        // Đảm bảo search container có position relative
        this.searchContainer.style.position = 'relative';
        this.searchContainer.appendChild(this.suggestionsContainer);
    }

    attachEventListeners() {
        // Event listener cho input
        this.searchInput.addEventListener('input', (e) => {
            this.handleInput(e.target.value);
        });

        // Event listener cho focus
        this.searchInput.addEventListener('focus', () => {
            if (this.searchInput.value.trim() !== '') {
                this.showSuggestions();
            }
        });

        // Event listener cho blur (ẩn suggestions khi click ra ngoài)
        document.addEventListener('click', (e) => {
            if (!this.searchContainer.contains(e.target)) {
                this.hideSuggestions();
            }
        });

        // Event listener cho arrow navigation
        this.searchInput.addEventListener('keydown', (e) => {
            const suggestions = this.suggestionsContainer?.querySelectorAll('.suggestion-item:not(.loading-state):not(.empty-state)');
            
            switch(e.key) {
                case 'Enter':
                    e.preventDefault();
                    if (this.selectedIndex >= 0 && suggestions && suggestions[this.selectedIndex]) {
                        // Nếu có suggestion được chọn, click vào nó
                        suggestions[this.selectedIndex].click();
                    }
                    // Không thực hiện search nếu không có suggestion nào được chọn
                    break;
                    
                case 'ArrowDown':
                    e.preventDefault();
                    if (suggestions && suggestions.length > 0) {
                        this.selectedIndex = Math.min(this.selectedIndex + 1, suggestions.length - 1);
                        this.updateSelectedSuggestion(suggestions);
                    }
                    break;
                    
                case 'ArrowUp':
                    e.preventDefault();
                    if (suggestions && suggestions.length > 0) {
                        this.selectedIndex = Math.max(this.selectedIndex - 1, -1);
                        this.updateSelectedSuggestion(suggestions);
                    }
                    break;
                    
                case 'Escape':
                    this.hideSuggestions();
                    this.selectedIndex = -1;
                    break;
            }
        });

        // Event listener cho search icon click
        const searchIcon = document.querySelector('.search-icon');
        if (searchIcon) {
            searchIcon.addEventListener('click', () => {
                this.performSearch(this.searchInput.value);
            });
        }
    }

    handleInput(query) {
        // Debounce để tránh gọi API quá nhiều
        clearTimeout(this.debounceTimer);
        
        if (query.trim() === '') {
            this.hideSuggestions();
            return;
        }

        // Hiển thị loading state
        this.showLoadingState();

        this.debounceTimer = setTimeout(() => {
            this.searchProducts(query);
        }, 300); // Đợi 300ms sau khi user ngừng gõ
    }

    showLoadingState() {
        if (!this.suggestionsContainer) return;
        
        this.suggestionsContainer.innerHTML = `
            <div class="suggestion-item loading-state" style="text-align: center; padding: 20px; color: #666;">
                <div>Đang tìm kiếm...</div>
            </div>
        `;
        this.showSuggestions();
    }

    async searchProducts(query) {
        try {
            // Kiểm tra nếu đang ở localhost thì dùng port 3000, nếu không thì dùng URL relative
            const baseUrl = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1' 
                ? 'http://localhost:3000' 
                : '';
            
            const response = await fetch(`${baseUrl}/api/products/search/${encodeURIComponent(query)}`);
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            
            const products = await response.json();
            this.displaySuggestions(products);
        } catch (error) {
            console.error('Error searching products:', error);
            this.hideSuggestions();
        }
    }

    displaySuggestions(products) {
        if (!products || products.length === 0) {
            this.showEmptyState();
            return;
        }

        this.suggestionsContainer.innerHTML = '';
        this.suggestions = products;
        this.selectedIndex = -1; // Reset selected index

        products.forEach((product, index) => {
            const suggestionItem = document.createElement('div');
            suggestionItem.className = 'suggestion-item';
            suggestionItem.dataset.index = index;

            // Tạo nội dung suggestion item
            const productImage = product.images && product.images.length > 0 ? product.images[0] : '';
            
            // Tính giá gốc và giá đã giảm
            const originalPrice = product.price;
            const discount = product.discount || 0;
            const discountedPrice = originalPrice - (originalPrice * discount / 100);
            
            // Format giá VNĐ
            const formattedOriginalPrice = new Intl.NumberFormat('vi-VN', {
                style: 'currency',
                currency: 'VND'
            }).format(originalPrice);
            
            const formattedDiscountedPrice = new Intl.NumberFormat('vi-VN', {
                style: 'currency',
                currency: 'VND'
            }).format(discountedPrice);

            suggestionItem.innerHTML = `
                ${productImage ? `<img src="${productImage}" alt="${product.name}">` : ''}
                <div class="product-info">
                    <div class="product-name-suggestion">${product.name}</div>
                    <div class="product-price-suggestion">
                        ${discount > 0 ? `
                            <span class="discounted-price">${formattedDiscountedPrice}</span>
                            <span class="original-price">${formattedOriginalPrice}</span>
                            <span class="discount-badge">-${Math.round(discount)}%</span>
                        ` : `
                            <span class="current-price">${formattedOriginalPrice}</span>
                        `}
                    </div>
                </div>
            `;
            console.log(`Suggestion item created for product: ${product.name}`, suggestionItem);
            // Event listeners cho suggestion item
            suggestionItem.addEventListener('click', () => {
                this.selectProduct(product);
            });

            suggestionItem.addEventListener('mouseenter', () => {
                this.selectedIndex = index;
                this.updateSelectedSuggestion();
            });

            this.suggestionsContainer.appendChild(suggestionItem);
        });

        this.showSuggestions();
    }

    updateSelectedSuggestion(suggestionElements = null) {
        const suggestions = suggestionElements || this.suggestionsContainer?.querySelectorAll('.suggestion-item:not(.loading-state):not(.empty-state)');
        
        if (!suggestions) return;

        // Remove selected class from all suggestions
        suggestions.forEach(item => item.classList.remove('selected'));

        // Add selected class to current suggestion
        if (this.selectedIndex >= 0 && suggestions[this.selectedIndex]) {
            suggestions[this.selectedIndex].classList.add('selected');
            
            // Scroll into view if needed
            suggestions[this.selectedIndex].scrollIntoView({
                block: 'nearest',
                behavior: 'smooth'
            });
        }
    }

    showEmptyState() {
        if (!this.suggestionsContainer) return;
        
        this.suggestionsContainer.innerHTML = `
            <div class="suggestion-item empty-state" style="text-align: center; padding: 20px; color: #999;">
                <div>Không tìm thấy sản phẩm nào</div>
            </div>
        `;
        this.showSuggestions();
    }

    selectProduct(product) {
        // Điền tên sản phẩm vào input
        this.searchInput.value = product.name;
        this.hideSuggestions();
        
        // Chuyển hướng đến trang chi tiết sản phẩm
        this.goToProductDetail(product._id);
    }

    goToProductDetail(productId) {
        // Chuyển hướng đến trang chi tiết sản phẩm
        window.location.href = `../detailPage/index.html?id=${productId}`;
    }

    performSearch(query) {
        if (query.trim() === '') {
            return;
        }

        // Ẩn suggestions
        this.hideSuggestions();
        
        // Chuyển hướng đến trang view all products với query
        window.location.href = `../view_all_products_page/all_products.html?search=${encodeURIComponent(query)}`;
    }

    showSuggestions() {
        this.suggestionsContainer.style.display = 'block';
        this.suggestionsContainer.classList.add('show');
    }

    hideSuggestions() {
        this.suggestionsContainer.style.display = 'none';
        this.suggestionsContainer.classList.remove('show');
        this.selectedIndex = -1; // Reset selected index
    }
}

// Khởi tạo search functionality khi DOM loaded
document.addEventListener('DOMContentLoaded', () => {
    new ProductSearch();
});

// Export cho các file khác có thể sử dụng
if (typeof module !== 'undefined' && module.exports) {
    module.exports = ProductSearch;
}