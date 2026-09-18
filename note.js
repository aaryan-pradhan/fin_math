// Shared MathJax setup for every Note: $…$ inline, $$…$$ display.
window.MathJax = { tex: { inlineMath: [['$', '$'], ['\\(', '\\)']] } };
document.head.appendChild(Object.assign(document.createElement('script'), {
  src: 'https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js', async: true
}));
