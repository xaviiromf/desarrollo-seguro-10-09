/**
 * Scripts de interacción y cálculo para la base de supermercado con soporte para Pesos Chilenos (CLP)
 * y opción "Sin precio definido".
 */

// Formato nativo es-CL (separador de miles "."), sin la regex con backtracking señalada por SonarQube (javascript:S8786).
const clpFormatter = new Intl.NumberFormat('es-CL', { maximumFractionDigits: 0 });

function formatCLP(amount) {
    return '$' + clpFormatter.format(Math.round(amount));
}

// Tacha o destacha el nombre usando nodos de texto: nunca innerHTML con datos del usuario (evita XSS en el DOM).
function applyPurchasedState(row, isPurchased) {
    const nameCell = row.querySelector('.item-name-cell');
    if (!nameCell) return;
    const name = nameCell.textContent.trim();
    if (isPurchased) {
        const strike = document.createElement('s');
        strike.textContent = name;
        nameCell.replaceChildren(strike);
        row.classList.add('bg-slate-50/70', 'text-slate-400');
    } else {
        nameCell.replaceChildren(document.createTextNode(name));
        row.classList.remove('bg-slate-50/70', 'text-slate-400');
    }
}

async function togglePurchased(form) {
    const response = await fetch(form.getAttribute('action'), {
        method: 'POST',
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': form.querySelector('[name=csrfmiddlewaretoken]').value,
        }
    });
    if (!response.ok) throw new Error('HTTP ' + response.status);
    return response.json();
}

document.addEventListener('DOMContentLoaded', () => {
    // 1. Calculadora reactiva en vivo en el formulario de agregar/editar producto
    const qtyInput = document.getElementById('id_quantity');
    const priceInput = document.getElementById('id_unit_price');
    const unknownPriceCheckbox = document.getElementById('id_has_unknown_price');
    const subtotalDisplay = document.getElementById('live-item-subtotal');

    function updateLiveSubtotal() {
        if (!subtotalDisplay) return;

        const isUnknown = unknownPriceCheckbox?.checked;

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
        const qty = Number.parseFloat(qtyInput ? qtyInput.value : 1) || 0;
        const price = Number.parseFloat(priceInput ? priceInput.value : 0) || 0;
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
            const row = form.closest('tr');
            try {
                const data = await togglePurchased(form);
                if (data.success && row) applyPurchasedState(row, data.is_purchased);
            } catch (err) {
                // Si falla la petición en segundo plano, se envía el formulario normal y el servidor decide.
                console.warn('No se pudo actualizar en segundo plano:', err);
                form.submit();
            }
        });
    });
});
