let products = [];

document.addEventListener('DOMContentLoaded', async () => {
    const response = await fetch('/api/products');
    products = await response.json();

    renderProducts(products); // gọi hàm hiển thị
    updateBodyHeightAndLine(); // cập nhật layout chiều cao

});


//Cập nhật chiều dài của trang
function updateBodyHeightAndLine() {
  const container = document.querySelector('.body');
  const line = document.querySelector('.line-4');
  if (!container || !line) return;

  let maxHeight = 0;
  const allChildren = container.querySelectorAll('*');
  const containerRect = container.getBoundingClientRect();

  allChildren.forEach(el => {
    const style = window.getComputedStyle(el);
    let elBottom;

    if (style.position === 'absolute' || style.position === 'fixed') {
      elBottom = el.offsetTop + el.offsetHeight;
    } else {
      const rect = el.getBoundingClientRect();
      elBottom = rect.bottom - containerRect.top;
    }

    if (elBottom > maxHeight) maxHeight = elBottom;
  });

  // Cập nhật chiều cao cho container
  container.style.height = maxHeight + 'px';

  // Cập nhật chiều dài cho .line-4 dựa trên chiều cao container
  line.style.width = (maxHeight - 55) + 'px';
}
window.addEventListener('load', () => {
  updateBodyHeightAndLine();
});


function renderProducts(products) {
  const productList = document.querySelector('.list-product');
  productList.innerHTML = ''; // Xoá hết nội dung cũ

  products.forEach(product => {
    // Tạo phần tử chứa sản phẩm
    const productElement = document.createElement('div');
    productElement.className = 'frame-940';

    productElement.innerHTML = `
      <a class="edit" href="edit.html?productId=${product._id}">
        <img src="images/edit.svg" alt="Edit" />
      </a>
      <button class="btn delete">
        <img src="images/delete.svg" alt="Delete" />
      </button>

      <a class="details" href="/product_management/view.html?id=${product._id}">Chi tiết</a>

      <div class="product-price">${product.price}</div>
      <div class="product-stock">${product.stock}</div>
      <div class="product-name">${product.name}</div>
      <div class="product-id">${product._id}</div>
    `;

    // Lấy nút xóa và gán sự kiện
    const deleteBtn = productElement.querySelector('.btn.delete');
    deleteBtn.addEventListener('click', async () => {
      console.log(product._id);
      if (confirm(`Bạn có chắc muốn xóa sản phẩm "${product.name}" không?`)) {
        await deleteProduct(product._id);
      }
    });

    productList.appendChild(productElement);
  });
}

// Hàm xóa sản phẩm
async function deleteProduct(productId) {
  try {
    const response = await fetch(`/api/products/${productId}`, { method: 'DELETE' });

    if (!response.ok) {
      alert('Xóa sản phẩm thất bại!');
      return;
    }

    // Lấy lại danh sách sản phẩm mới
    const refreshedResponse = await fetch('/api/products');
    const updatedProducts = await refreshedResponse.json();

    // Cập nhật lại giao diện
    renderProducts(updatedProducts);
    updateBodyHeightAndLine();

  } catch (error) {
    alert('Lỗi khi xóa sản phẩm');
    console.error(error);
  }
}




const searchInput = document.getElementById('searchInput');
const clearBtn = document.getElementById('clearSearch');

// Khi người dùng gõ
searchInput.addEventListener('input', () => {
  const keyword = searchInput.value.toLowerCase().trim();

  const filtered = products.filter(product =>
    product.name.toLowerCase().includes(keyword) ||
    product._id.toLowerCase().includes(keyword)
  );


  renderProducts(filtered);
  updateBodyHeightAndLine();
});


// Xóa tìm kiếm
clearBtn.addEventListener('click', () => {
  searchInput.value = '';
  renderProducts(products);
  updateBodyHeightAndLine();
});



// Lọc sản phẩm
const statusFilter = document.getElementById('status-filter');

statusFilter.addEventListener('change', () => {
  const selectedCategory = statusFilter.value;

  if (selectedCategory === 'all') {
    renderProducts(products);
  } else {
    const filtered = products.filter(product =>
      product.category && product.category === selectedCategory
    );
    renderProducts(filtered);
  }

  updateBodyHeightAndLine();
});