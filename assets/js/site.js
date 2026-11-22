// Envoi du formulaire de contact (Formspree) sans quitter la page. Sans JavaScript, le formulaire s'envoie normalement.
document.querySelectorAll('form.formulaire').forEach((form) => {
  const etat = form.querySelector('.formulaire-etat');
  const bouton = form.querySelector('button[type="submit"]');
  const libelle = bouton.textContent;
  form.addEventListener('submit', async (ev) => {
    ev.preventDefault();
    bouton.disabled = true;
    bouton.textContent = form.dataset.envoi;
    try {
      const donnees = Object.fromEntries(new FormData(form));
      const r = await fetch(form.dataset.ajax || form.action, {
        method: 'POST', body: JSON.stringify(donnees),
        headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
      });
      if (!r.ok) throw new Error(r.status);
      form.reset();
      etat.textContent = form.dataset.succes;
    } catch (e) {
      etat.textContent = form.dataset.erreur;
    } finally {
      bouton.disabled = false;
      bouton.textContent = libelle;
    }
  });
});
