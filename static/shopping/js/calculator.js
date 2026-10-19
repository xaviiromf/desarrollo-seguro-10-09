/**
 * Scripts de interacción y cálculo para la base de supermercado con soporte para Pesos Chilenos (CLP)
 * y opción "Sin precio definido".
 */

// Formato nativo es-CL (separador de miles "."), sin la regex con backtracking señalada por SonarQube (javascript:S8786).
const clpFormatter = new Intl.NumberFormat('es-CL', { maximumFractionDigits: 0 });

function formatCLP(amount) {
    return '$' + clpFormatter.format(Math.round(amount));
}

document.addEventListener('DOMContentLoaded', () => {
    // 1. Calculadora reactiva en vivo en el formulario de agregar/editar producto
    const qtyInput = document.getElementById('id_quantity');
    const priceInput = document.getElementById('id_unit_price');
    const unknownPriceCheckbox = document.getElementById('id_has_unknown_price');
    const subtotalDisplay = document.getElementById('live-item-subtotal');

    function updateLiveSubtotal() {
        if (!subtotalDisplay) return;

        const isUnknown = unknownPriceCheckbox && unknownPriceCheckbox.checked;

        if (priceInput) {
            if (isUnknown) {
                priceInput.disabled = true;
                priceInput.classList.add('bg-slate-100', 'cursor-not-allowed', 'opacity-60');
            } else {
                priceInput.disabled = false;
                priceInput.classList.remove('bg-slate-100', 'cursor-not-allowed', 'opacity-60');
            }
        }

        if (isUnknown) {
            subtotalDisplay.textContent = 'Sin precio (Por confirmar)';
            subtotalDisplay.className = 'text-sm font-semibold text-amber-600 italic';
            return;
        }

        subtotalDisplay.className = 'text-base font-extrabold text-emerald-800';
        const qty = parseFloat(qtyInput ? qtyInput.value : 1) || 0;
        const price = parseFloat(priceInput ? priceInput.value : 0) || 0;
        const total = Math.round(qty * price);

        subtotalDisplay.textContent = formatCLP(total);
    }

    if (qtyInput) qtyInput.addEventListener('input', updateLiveSubtotal);
    if (priceInput) priceInput.addEventListener('input', updateLiveSubtotal);
    if (unknownPriceCheckbox) unknownPriceCheckbox.addEventListener('change', updateLiveSubtotal);

    // Inicializar cálculo al cargar
    updateLiveSubtotal();

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
                                row.classList.add('bg-slate-50/70', 'text-slate-400');
                            } else {
                                if (nameCell.querySelector('s')) {
                                    nameCell.innerHTML = nameCell.querySelector('s').textContent.trim();
                                }
                                row.classList.remove('bg-slate-50/70', 'text-slate-400');
                            }
                        }
                    }
                } else {
                    form.submit();
                }
            } catch (err) {
                form.submit();
            }
        });
    });
});
