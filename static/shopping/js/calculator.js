/**
 * Scripts de interacción y cálculo para la base HTML del supermercado
 */

document.addEventListener('DOMContentLoaded', () => {
    // 1. Calculadora reactiva en vivo en el formulario de agregar/editar producto
    const qtyInput = document.getElementById('id_quantity');
    const priceInput = document.getElementById('id_unit_price');
    const subtotalDisplay = document.getElementById('live-item-subtotal');

    function updateLiveSubtotal() {
        if (!qtyInput || !priceInput || !subtotalDisplay) return;
        
        const qty = parseFloat(qtyInput.value) || 0;
        const price = parseFloat(priceInput.value) || 0;
        const total = (qty * price).toFixed(2);
        
        subtotalDisplay.textContent = `$${Number(total).toLocaleString('es-CL', {
            minimumFractionDigits: 2,
            maximumFractionDigits: 2
        })}`;
    }

    if (qtyInput && priceInput) {
        qtyInput.addEventListener('input', updateLiveSubtotal);
        priceInput.addEventListener('input', updateLiveSubtotal);
        // Inicializar cálculo al cargar la página
        updateLiveSubtotal();
    }

    // 2. Alternancia reactiva de ítems comprados vía AJAX
    const purchaseToggles = document.querySelectorAll('.js-toggle-purchased');
    purchaseToggles.forEach(toggle => {
        toggle.addEventListener('change', async (e) => {
            const form = e.target.closest('form');
            if (!form) return;

            const url = form.getAttribute('action');
            const row = form.closest('tr');
            const csrfToken = form.querySelector('[name=csrfmiddlewaretoken]').value;

            try {
                const response = await fetch(url, {
                    method: 'POST',
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest',
                        'X-CSRFToken': csrfToken,
                    }
                });

                if (response.ok) {
                    const data = await response.json();
                    if (data.success && row) {
                        const nameCell = row.querySelector('.item-name-cell');
                        if (nameCell) {
                            if (data.is_purchased) {
                                if (!nameCell.querySelector('s')) {
                                    nameCell.innerHTML = `<s>${nameCell.textContent.trim()}</s>`;
                                }
                            } else {
                                if (nameCell.querySelector('s')) {
                                    nameCell.innerHTML = nameCell.querySelector('s').textContent.trim();
                                }
                            }
                        }
                    }
                } else {
                    // Fallback a envío convencional de formulario
                    form.submit();
                }
            } catch (err) {
                form.submit();
            }
        });
    });
});
