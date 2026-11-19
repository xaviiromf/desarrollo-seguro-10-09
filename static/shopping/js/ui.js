/**
 * Comportamiento de la interfaz que antes estaba en atributos onclick/onchange/onsubmit y en un <script>
 * en línea. Vive en un archivo propio para que la Content Security Policy pueda prohibir el código en línea.
 */
document.addEventListener('DOMContentLoaded', () => {
    // Anchos de las barras de progreso (antes style="width: ..%"). El CSSOM no está limitado por la CSP.
    document.querySelectorAll('[data-width]').forEach((bar) => {
        const pct = Math.min(Math.max(Number.parseFloat(bar.dataset.width) || 0, 0), 100);
        bar.style.width = pct + '%';
    });

    // Confirmación antes de enviar formularios destructivos. El texto se lee como dato, nunca se ejecuta.
    document.querySelectorAll('form[data-confirm]').forEach((form) => {
        form.addEventListener('submit', (e) => {
            if (!window.confirm(form.dataset.confirm)) e.preventDefault();
        });
    });

    document.querySelectorAll('[data-action="print"]').forEach((btn) => btn.addEventListener('click', () => window.print()));
    document.querySelectorAll('select[data-autosubmit]').forEach((sel) => sel.addEventListener('change', () => sel.form.submit()));

    const toast = document.getElementById('toast-notification');
    function showToast(message) {
        if (!toast) return;
        toast.textContent = message;
        toast.classList.remove('opacity-0', 'pointer-events-none');
        toast.classList.add('opacity-100');
        setTimeout(() => {
            toast.classList.remove('opacity-100');
            toast.classList.add('opacity-0', 'pointer-events-none');
        }, 2500);
    }

    // Copiar la lista para WhatsApp: el texto lo arma el servidor en un <textarea hidden> con escape HTML.
    const btnWhatsapp = document.getElementById('btn-copy-whatsapp');
    const whatsappText = document.getElementById('whatsapp-text');
    if (btnWhatsapp && whatsappText) {
        btnWhatsapp.addEventListener('click', () => {
            navigator.clipboard.writeText(whatsappText.value)
                .then(() => showToast('¡Lista copiada al portapapeles para WhatsApp! 📋'))
                .catch(() => showToast('No se pudo copiar automáticamente'));
        });
    }

    // Buscador en tiempo real de productos en la tabla.
    const liveSearchInput = document.getElementById('live-table-search');
    if (liveSearchInput) {
        liveSearchInput.addEventListener('input', (e) => {
            const query = e.target.value.toLowerCase().trim();
            document.querySelectorAll('#products-table tbody tr').forEach((row) => {
                row.style.display = row.textContent.toLowerCase().includes(query) ? '' : 'none';
            });
        });
    }
});
