document.addEventListener('DOMContentLoaded', () => {
  const container = document.querySelector('.frame-768');
  const template = container.querySelector('.frame-558');

  const menuData = [
    {
      label: 'Laptop',
      category: 'Laptop',
      dropdown: [
        {
          title: 'Thương hiệu',
          items: ['MSI', 'DELL', 'ACER', 'LENOVO', 'ASUS']
        },
        {
          title: 'Mức giá',
          items: [
            { label: 'Từ 10–20 triệu', value: '10-20' },
            { label: 'Từ 20 – 30 triệu', value: '20-30' },
            { label: 'Trên 30 triệu', value: '30+' }
          ]
        }
      ]
    },
    {
      label: 'Laptop Gaming',
      category: 'LaptopGaming',
      dropdown: [
        {
          title: 'Thương hiệu',
          items: ['MSI', 'DELL', 'ACER', 'LENOVO', 'ASUS']
        },
        {
          title: 'Mức giá',
          items: [
            { label: 'Từ 10–20 triệu', value: '10-20' },
            { label: 'Từ 20 – 30 triệu', value: '20-30' },
            { label: 'Trên 30 triệu', value: '30+' }
          ]
        }
      ]
    },
    {
      label: 'Chuột',
      category: 'Mouse',
      dropdown: [
        {
          title: 'Thương hiệu',
          items: ['Logitech', 'Razer', 'Corsair']
        },
        {
          title: 'Mức giá',
          items: [
            { label: 'Dưới 1 triệu', value: '<1' },
            { label: '1 - 3 triệu', value: '1-3' },
            { label: 'Trên 3 triệu', value: '3+' }
          ]
        }
      ]
    },
    {
      label: 'Bàn phím',
      category: 'Keyboard',
      dropdown: [
        {
          title: 'Thương hiệu',
          items: ['Akko', 'DareU']
        },
        {
          title: 'Mức giá',
          items: [
            { label: 'Dưới 1 triệu', value: '<1' },
            { label: '1 - 3 triệu', value: '1-3' },
            { label: 'Trên 3 triệu', value: '3+' }
          ]
        }
      ]
    }
  ];

  function buildDropdown(category, dropdown) {
    const menu = document.createElement('div');
    menu.className = 'dropdown-menu';

    dropdown.forEach(cat => {
      const categoryEl = document.createElement('div');
      categoryEl.className = 'category';

      const title = document.createElement('div');
      title.className = 'title';
      title.textContent = cat.title;
      title.style.fontWeight = 'bold';
      title.style.marginBottom = '8px';
      title.style.color = '#222';
      categoryEl.appendChild(title);

      cat.items.forEach(item => {
        const a = document.createElement('a');
        a.href = '#';

        if (typeof item === 'string') {
          // Brand item
          a.textContent = item;
          a.onclick = (e) => {
            e.preventDefault();
            window.location.href = `../view_all_products_page/all_products.html?category=${encodeURIComponent(category)}&brand=${encodeURIComponent(item)}`;
          };
        } else {
          // Price item
          a.textContent = item.label;
          a.onclick = (e) => {
            e.preventDefault();
            window.location.href = `../view_all_products_page/all_products.html?category=${encodeURIComponent(category)}&price=${encodeURIComponent(item.value)}`;
          };
        }

        categoryEl.appendChild(a);
      });

      menu.appendChild(categoryEl);
    });

    return menu;
  }

  menuData.forEach((item, i) => {
    const { label, category, dropdown } = item;

    if (i === 0) {
      const labelEl = template.querySelector('div.laptop');
      labelEl.textContent = label;
      labelEl.onclick = () => {
        window.location.href = `../view_all_products_page/all_products.html?category=${encodeURIComponent(category)}`;
      };

      const oldDropdown = template.querySelector('.dropdown-menu');
      oldDropdown.replaceWith(buildDropdown(category, dropdown));
      return;
    }

    const clone = template.cloneNode(true);
    const labelEl = clone.querySelector('div.laptop');
    labelEl.textContent = label;
    labelEl.onclick = () => {
      window.location.href = `../view_all_products_page/all_products.html?category=${encodeURIComponent(category)}`;
    };

    const oldDropdown = clone.querySelector('.dropdown-menu');
    oldDropdown.replaceWith(buildDropdown(category, dropdown));
    container.appendChild(clone);
  });
});
