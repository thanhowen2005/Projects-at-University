
// Lấy thông tin sản phẩm cần xem
function getProductIdFromURL() {
  const params = new URLSearchParams(window.location.search);
  return params.get('id'); // Lấy id từ ?id=...
}

async function getProductFromURL() {
  const id = getProductIdFromURL();
  if (!id) throw new Error('No product ID in URL');

  const res = await fetch(`/api/products/${id}`);
  if (!res.ok) throw new Error('Product not found');

  return await res.json();
}


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



//Hiện thông tin điền theo đúng phân loại danh mục sản phẩm
const specsMapping = {
  Laptop: {
    warranty: "Thời gian bảo hành",
    color: "Màu sắc",
    cpu: "CPU",
    card: "Card",
    screen: "Màn hình",
    memory: "Dung lượng RAM",
    hardware: "Ổ cứng",
    camera: "Camera",
    battery: "Dung lượng Pin",
    weight: "Cân nặng",
  },
  LaptopGaming: {
    warranty: "Thời gian bảo hành",
    color: "Màu sắc",
    cpu: "CPU",
    card: "Card",
    screen: "Màn hình",
    memory: "Dung lượng RAM",
    hardware: "Ổ cứng",
    camera: "Camera",
    battery: "Dung lượng Pin",
    weight: "Cân nặng",
  },
  Mouse: {
    warranty: "Thời gian bảo hành",
    color: "Màu sắc",
    dpi: "DPI",
    pin: "Pin",
    memory: "Bộ nhớ kết hợp",
    height: "Chiều cao",
    weight: "Cân nặng",
  },
  Keyboard: {
    warranty: "Thời gian bảo hành",
    color: "Màu sắc",
    size: "Kích thước",
    pin: "Pin",
    switch: "Switch",
    led: "LED",
    connection: "Kết nối",
    keycap: "Keycap",
    weight: "Trọng lượng",
  }
};


//Hiển thị các thông tin chung
function formatPrice(price) {
  return price.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",") + " ₫";
}

function fillProductInfo(product) {
    // Tên sản phẩm
    const nameEl = document.getElementById("product-name");
    if (nameEl) nameEl.textContent = product.name || "";

    // Giá thành
    const priceEl = document.getElementById("product-price");
    if (priceEl) priceEl.textContent = product.price ? formatPrice(product.price) : "";

    // Danh mục
    const categoryEl = document.getElementById("category-name");
    if (categoryEl) categoryEl.textContent = product.category || "";

    // Thương hiệu (lấy specs[0])
    const brandEl = document.getElementById("product-brand");
    if (brandEl) brandEl.textContent = product.specs?.[0] || "";

    // Thông tin mô tả
    const descriptionEl = document.getElementById("product-description");
    if (descriptionEl) descriptionEl.textContent = product.description || "";

    // Điểm nổi bật
    const highlightContainer = document.querySelector(".highlight-container");
    if (highlightContainer) {
    highlightContainer.innerHTML = ""; // Xoá input ban đầu nếu có

    product.highlights.forEach((text, i) => {
        const wrapper = document.createElement("div");
        wrapper.className = "placebox-info16"; // dùng lại class đang styled sẵn

        const box = document.createElement("div");
        box.className = "place-to-info-box";
        box.textContent = text;

        wrapper.appendChild(box);
        highlightContainer.appendChild(wrapper);
    });
    }

    // Link ảnh (4 link)
    for (let i = 0; i < 4; i++) {
    const imgEl = document.querySelector(`.placebox-info18${i + 1} .place-to-info-box`);
    if (imgEl) imgEl.textContent = product.images[i] || "";
    }

    // Tồn kho
    const stockEl = document.querySelector(".placebox-info19 .place-to-info-box");
    if (stockEl) stockEl.textContent = product.stock ?? "";

    // Giảm giá
    const discountEl = document.querySelector(".placebox-info20 .place-to-info-box");
    if (discountEl) discountEl.textContent = product.discount ? product.discount + "%" : "0%";

    // Ngày nhập kho
    const dateEl = document.querySelector(".placebox-info21 .place-to-info-box");
    if (dateEl) dateEl.textContent = product.date ? product.date : "";

    // Số lượng đã bán
    const soldEl = document.querySelector(".placebox-info22 .place-to-info-box");
    if (soldEl) soldEl.textContent = product.sold ? product.sold : 0;
}



//Hiển thị thông số chi tiết của sản phẩm
function displaySpecs(product) {
  const wrapper = document.getElementById("specs-wrapper");
  if (!wrapper) return;

  // Xóa hết nội dung cũ trong specs-wrapper
  wrapper.innerHTML = "";

  // Lấy thông tin specs label từ specsMapping dựa theo category
  // specsMapping ví dụ có dạng { Mouse: ["Thương hiệu", "Thời gian bảo hành", ...], ... }
  const specsLabelsObj = specsMapping[product.category];
  if (!specsLabelsObj) return;

  const specsLabels = Object.values(specsLabelsObj);
  // Các vị trí base và khoảng cách
  const baseTopLabel = 735;
  const baseTopInput = 722;
  const gap = 70;

  specsLabels.forEach((label, index) => {
    // Tạo div label với class info{index+1}
    const labelDiv = document.createElement("div");
    labelDiv.className = `info${index + 5}`;
    labelDiv.textContent = label;
    labelDiv.style.position = "absolute";
    labelDiv.style.left = "330px";
    labelDiv.style.top = `${baseTopLabel + gap * index}px`;
    labelDiv.style.color = "#000";
    labelDiv.style.textAlign = "right";
    labelDiv.style.fontFamily = `"Poppins-Regular", sans-serif`;
    labelDiv.style.fontSize = "16px";
    labelDiv.style.lineHeight = "24px";
    labelDiv.style.fontWeight = "400";

    // Tạo div chứa giá trị specs với class placebox-info{index+1}
    const inputDiv = document.createElement("div");
    inputDiv.className = `placebox-info${index + 5}`;
    inputDiv.style.position = "absolute";
    inputDiv.style.left = "503px";
    inputDiv.style.top = `${baseTopInput + gap * index}px`;
    inputDiv.style.width = "249px";
    inputDiv.style.height = "50px";

    // Tạo div hiển thị thông tin specs, class place-to-info-box
    const valueDiv = document.createElement("div");
    valueDiv.className = "place-to-info-box";
    // Hiển thị giá trị specs tương ứng (nếu không có thì để trống)
    valueDiv.textContent = product.specs[index + 1] || "";
    valueDiv.style.fontSize = "16px";
    valueDiv.style.padding = "10px";
    valueDiv.style.height = "100%";
    valueDiv.style.display = "flex";
    valueDiv.style.alignItems = "center";

    // Gắn valueDiv vào inputDiv, gắn labelDiv và inputDiv vào wrapper
    inputDiv.appendChild(valueDiv);
    wrapper.appendChild(labelDiv);
    wrapper.appendChild(inputDiv);
  });
}



document.addEventListener('DOMContentLoaded', async () => {
  try {
    updateBodyHeightAndLine();
    const product = await getProductFromURL();
    fillProductInfo(product);
    displaySpecs(product);
  } catch (error) {
    console.error(error);
  }
});


