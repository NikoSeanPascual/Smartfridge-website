document.addEventListener('DOMContentLoaded', () => {
    const themeToggle = document.getElementById('theme-toggle');

    if (localStorage.getItem('theme') === 'dark') {
        document.body.classList.add('dark-mode');
        themeToggle.textContent = '☀️';
    }

    if (themeToggle) {
        themeToggle.addEventListener('click', () => {
            document.body.classList.toggle('dark-mode');
            if (document.body.classList.contains('dark-mode')) {
                localStorage.setItem('theme', 'dark');
                themeToggle.textContent = '☀️';
            } else {
                localStorage.setItem('theme', 'light');
                themeToggle.textContent = '🌙';
            }
        });
    }

    function getCSRFToken() {
        const csrfInput = document.querySelector('[name=csrfmiddlewaretoken]');
        return csrfInput ? csrfInput.value : '';
    }

    const addForm = document.getElementById('add-item-form');
    const pantryGrid = document.getElementById('pantry-grid');

    if (addForm) {
        addForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const ingredientName = document.getElementById('ingredient-input').value;
            const quantity = document.getElementById('quantity-input').value;

            try {
                const response = await fetch('/api/add/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCSRFToken()
                    },
                    body: JSON.stringify({ ingredient_name: ingredientName, quantity: quantity })
                });

                const data = await response.json();

                if (data.status === 'success') {
                    const emptyMsg = document.getElementById('empty-msg');
                    if (emptyMsg) emptyMsg.remove();

                    let badgeClass = data.is_expired ? 'badge-danger' : (data.is_expiring_soon ? 'badge-warning' : 'badge-success');
                    let badgeText = data.is_expired ? 'Expired' : (data.is_expiring_soon ? 'Expiring Soon' : 'Fresh');
                    let cardClass = data.is_expired ? 'expired' : (data.is_expiring_soon ? 'expiring' : '');

                    const cardHTML = `
                        <div class="pantry-card ${cardClass}" id="item-card-${data.item_id}" style="animation: popIn 0.3s ease-out;">
                            <div class="card-header">
                                <h4>${data.name}</h4>
                                <span class="category-tag">${data.category}</span>
                            </div>
                            <div class="card-body">
                                <p><strong>Quantity:</strong> ${data.quantity}</p>
                                <p><strong>Expires:</strong> ${data.exp_date}</p>
                                <span class="badge ${badgeClass}">${badgeText}</span>
                            </div>
                            <div class="card-footer">
                                <button class="btn btn-danger btn-sm delete-btn" data-id="${data.item_id}">Consume / Remove</button>
                            </div>
                        </div>
                    `;
                    pantryGrid.insertAdjacentHTML('afterbegin', cardHTML);
                    addForm.reset();
                } else {
                    alert(data.message);
                }
            } catch (err) {
                console.error(err);
            }
        });
    }

    if (pantryGrid) {
        pantryGrid.addEventListener('click', async (e) => {
            if (e.target.classList.contains('delete-btn')) {
                const itemId = e.target.getAttribute('data-id');
                const card = document.getElementById(`item-card-${itemId}`);

                card.style.transform = 'scale(0.8)';
                card.style.opacity = '0';
                card.style.transition = 'all 0.3s ease';

                setTimeout(async () => {
                    const response = await fetch(`/api/delete/${itemId}/`, {
                        method: 'POST',
                        headers: { 'X-CSRFToken': getCSRFToken() }
                    });
                    const data = await response.json();
                    if (data.status === 'success') { card.remove(); }
                }, 300);
            }
        });
    }
});