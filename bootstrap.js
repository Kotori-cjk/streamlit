const status = document.getElementById('runtime-status');

try {
  const response = await fetch('public-files.json', { cache: 'no-cache' });
  if (!response.ok) throw new Error(`文件清单加载失败（${response.status}）`);
  const manifest = await response.json();
  const files = Object.fromEntries(manifest.files.map(path => {
    const url = new URL(path, location.href);
    if (manifest.revision) url.searchParams.set('v', manifest.revision);
    return [path, { url: url.href }];
  }));
  files['site_base.json'] = JSON.stringify({ base_url: new URL('./', location.href).href });
  const { mount } = await import('https://cdn.jsdelivr.net/npm/@stlite/browser@0.85.1/build/stlite.js');
  mount({
    entrypoint: 'app.py',
    files,
    requirements: manifest.requirements || [],
    streamlitConfig: {
      'client.toolbarMode': 'viewer',
      'theme.primaryColor': '#527d70',
      'theme.backgroundColor': '#fffdf8',
      'theme.secondaryBackgroundColor': '#f1eee6',
      'theme.textColor': '#403b4e',
    },
  }, document.getElementById('app'));
} catch (error) {
  status.textContent = `交互视图暂时未能启动：${error.message}。请打开“快速视频预览”查看样本。`;
  status.classList.add('load-error');
}
