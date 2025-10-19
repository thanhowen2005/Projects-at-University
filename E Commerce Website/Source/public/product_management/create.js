const menuData = [
  {
    _id: "683dbf577f1c1ec918a1e53c",
    label: "Laptop",
    url: "/laptop",
    order: 1,
    dropdown: [
      {
        title: "Theo dòng",
        items: [
          { label: "MSI", url: "/laptop/msi" },
          { label: "DELL", url: "/laptop/dell" },
          { label: "ACER", url: "/laptop/acer" },
          { label: "Lenovo", url: "/mouse/lenovo" },
          { label: "Dell", url: "/mouse/dell" },
          { label: "HP", url: "/mouse/corsair" },
        ]
      },
      {
        title: "Theo giá tiền",
        items: [
          { label: "Dưới 10 triệu", url: "/laptop/duoi-10-trieu" },
          { label: "Từ 10–20 triệu", url: "/laptop/10-20-trieu" },
          { label: "Trên 20 triệu", url: "/laptop/tren-20-trieu" }
        ]
      }
    ]
  },
    {
    _id: "683dbf577f1c1ec918a1e53d",
    label: "LaptopGaming",
    url: "/laptop-gaming",
    order: 2,
    dropdown: [
      {
        title: "Theo dòng",
        items: [
          { label: "MSI", url: "/laptop/msi" },
          { label: "DELL", url: "/laptop/dell" },
          { label: "ACER", url: "/laptop/acer" },
          { label: "Lenovo", url: "/mouse/lenovo" },
          { label: "Dell", url: "/mouse/dell" },
          { label: "HP", url: "/mouse/corsair" },
        ]
      },
      {
        title: "Theo giá tiền",
        items: [
          { label: "Dưới 10 triệu", url: "/laptop/duoi-10-trieu" },
          { label: "Từ 10–20 triệu", url: "/laptop/10-20-trieu" },
          { label: "Trên 20 triệu", url: "/laptop/tren-20-trieu" }
        ]
      }
    ]
  },
  {
    _id: "683dc02a7f1c1ec918a1e53e",
    label: "Mouse",
    url: "/mouse",
    order: 3,
    dropdown: [
      {
        title: "Thương hiệu",
        items: [
          { label: "Logitech", url: "/mouse/logitech" },
          { label: "Razer", url: "/mouse/razer" },
        ]
      },
      {
        title: "Theo giá tiền",
        items: [
          { label: "Dưới 500k", url: "/mouse/duoi-500k" },
          { label: "500k–1 triệu", url: "/mouse/500k-1-trieu" },
          { label: "Trên 1 triệu", url: "/mouse/tren-1-trieu" }
        ]
      }
    ]
  },
  {
    _id: "683dc12b7f1c1ec918a1e53f",
    label: "Keyboard",
    url: "/keyboard",
    order: 4,
    dropdown: [
      {
        title: "Theo dòng",
        items: [
          { label: "Akko", url: "/keyboard/akko" },
          { label: "Keychron", url: "/keyboard/keychron" },
          { label: "DareU", url: "/keyboard/dareu" }
        ]
      },
      {
        title: "Theo giá tiền",
        items: [
          { label: "< 1 triệu", url: "/keyboard/duoi-1-trieu" },
          { label: "1–3 triệu", url: "/keyboard/1-3-trieu" },
          { label: "> 3 triệu", url: "/keyboard/tren-3-trieu" }
        ]
      }
    ]
  }
];

///Update kich thuoc trang
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
  container.style.height = (maxHeight) + 'px';

  // Cập nhật chiều dài cho .line-4 dựa trên chiều cao container
  line.style.width = (maxHeight - 55) + 'px';
}
window.addEventListener('load', () => {
  updateBodyHeightAndLine();
});


////Thêm highlight cho sản phẩm
function addHighlightField() {
  const container = document.querySelector('.highlight-container');

  const newBox = document.createElement('div');
  newBox.className = 'placebox-info16';

  const input = document.createElement('input');
  input.type = 'text';
  input.placeholder = 'Điểm nổi bật';
  input.className = 'place-to-info-box';

  const md = document.createElement('div');
  md.className = 'md';
  md.textContent = 'Md';

  newBox.appendChild(input);
  newBox.appendChild(md);
  container.appendChild(newBox);
  updateBodyHeightAndLine();
}

document.addEventListener('DOMContentLoaded', () => {
  document.getElementById('add-highlight-btn').addEventListener('click', addHighlightField);
});





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

function populateCategorySelect(menuData) {
  const categorySelect = document.getElementById('category-select');
  if (!categorySelect) return;

  categorySelect.innerHTML = '';

  menuData.forEach(category => {
    const option = document.createElement('option');
    option.value = category.label; 
    option.textContent = category.label;
    categorySelect.appendChild(option);
  });
}


// Hàm tạo specs fields
function generateSpecsFields(category) {
  const wrapper = document.getElementById("specs-wrapper");
  if (!wrapper || !specsMapping[category]) return;

  wrapper.innerHTML = ""; // Xóa hết dòng specs cũ

   const specs = Object.values(specsMapping[category]);
  const baseTopLabel = 735; // vị trí dòng label đầu
  const baseTopInput = 722; // vị trí input đầu
  const gap = 70; // khoảng cách mỗi dòng

  specs.forEach((label, index) => {
    // Tạo label div
    const labelDiv = document.createElement("div");
    labelDiv.className = `infor${index + 1}`;
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

    // Tạo div chứa input
    const inputDiv = document.createElement("div");
    inputDiv.className = `placebox-info${index + 1}`;
    inputDiv.style.position = "absolute";
    inputDiv.style.left = "503px";
    inputDiv.style.top = `${baseTopInput + gap * index}px`;
    inputDiv.style.width = "249px";
    inputDiv.style.height = "50px";

    // Tạo input
    const input = document.createElement("input");
    input.type = "text";
    input.className = "place-to-info-box";
    input.placeholder = label;
    input.style.width = "100%";
    input.style.height = "100%";
    input.style.fontSize = "16px";
    input.style.padding = "10px";

    inputDiv.appendChild(input);
    wrapper.appendChild(labelDiv);
    wrapper.appendChild(inputDiv);
  });
}


// Hàm lấy thông tin sản phẩm từ input
function getProductFromForm() {
  const name = document.getElementById("product-name-input").value.trim();
  const price = Number(document.getElementById("product-price-input").value);
  const category = document.getElementById("category-select").value;
  const description = document.getElementById("product-description-input").value.trim();

  // Lấy brand riêng (specs[0])
    const brandInput = document.getElementById("product-brand-input").value.trim();


  // Lấy các specs còn lại từ specs-wrapper
  const specsInputs = document.querySelectorAll("#specs-wrapper input");
  const otherSpecs = Array.from(specsInputs).map(input => input.value.trim());

  // Gộp brand vào đầu mảng specs
  const specs = [brandInput, ...otherSpecs];

  // Lấy highlights
  const highlightInputs = document.querySelectorAll(".highlight-container input");
  const highlights = Array.from(highlightInputs).map(input => input.value.trim());

  // Lấy 4 ảnh
  const images = [];
  for (let i = 0; i < 4; i++) {
    const imgInput = document.getElementById(`image-link-${i + 1}`);
    if (imgInput) images.push(imgInput.value.trim());
  }

  const stock = Number(document.getElementById("product-stock-input").value);
  const discount = Number(document.getElementById("product-discount-input").value);
  const date = document.getElementById("product-date-input").value;
  const sold = 0

    // Kiểm tra trường nào bị thiếu
  if (
    !name || !price || !category || !description ||
    specs.some(spec => !spec) ||
    highlights.some(h => !h) ||
    images.some(img => !img) ||
    !stock || !discount || !date
  ) {
    alert("Vui lòng nhập đầy đủ thông tin sản phẩm trước khi tạo.");
    return null;
  }
  const product = {
    name,
    price,
    category,
    description,
    specs,              
    highlights,
    images,
    stock,
    discount,
    date,
    sold
  };
  return product;
}



// Khởi tạo dropdown & sự kiện onchange
document.addEventListener("DOMContentLoaded", () => {
  populateCategorySelect(menuData);

  const categorySelect = document.getElementById("category-select");
  categorySelect.addEventListener("change", function () {
    const selectedCategory = this.value;
    if (selectedCategory) {
      generateSpecsFields(selectedCategory);
    } else {
      document.getElementById("specs-wrapper").innerHTML = "";
    }
  });
});


async function addProduct() {
    const confirmAdd = confirm("Bạn có chắc chắn muốn tạo sản phẩm này?");
    if (!confirmAdd) return;

    const product = getProductFromForm();

    if (!product)
      return
    await fetch('/api/products', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(product)
    });

    window.location.href = 'index.html';
}

document.addEventListener("DOMContentLoaded", () => {
  document.getElementById("submit-btn").addEventListener("click", addProduct);
});


