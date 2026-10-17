const root = document.getElementById('samples');

function element(tag, text, className) {
  const node = document.createElement(tag);
  if (text !== undefined) node.textContent = text;
  if (className) node.className = className;
  return node;
}

function renderSample(sample, container) {
  const video = element('video', undefined, 'sample-video');
  video.src = sample.video;
  video.poster = sample.thumbnail;
  video.controls = true;
  video.playsInline = true;
  video.preload = 'metadata';
  video.setAttribute('aria-label', `${sample.group} · ${sample.title} · A/B 双视角视频`);
  const metrics = element('dl', undefined, 'sample-metrics');
  for (const [label, value] of [
    ['原交付尺寸', `${sample.width} × ${sample.height}`],
    ['帧数 / FPS', `${sample.frames} / ${sample.fps}`],
    ['首末 PTS 跨度', `${sample.pts_span_s} s`],
    ['LTX latent 时刻', sample.latent_frames],
  ]) {
    const cell = element('div');
    cell.append(element('dt', label), element('dd', value));
    metrics.append(cell);
  }
  const conditions = element('dl', undefined, 'sample-metrics');
  for (const [label, value] of Object.entries(sample.conditions)) {
    const cell = element('div');
    cell.append(element('dt', label), element('dd', value));
    conditions.append(cell);
  }
  const details = element('details', undefined, 'sample-details');
  details.append(element('summary', '查看数值质检与 loader 证据'), element('pre', JSON.stringify(sample.qc, null, 2)));
  const notes = element('ul', undefined, 'sample-caption');
  for (const note of sample.notes) notes.append(element('li', note));
  const cameraLink = element('a', '查看相机 JSON ↗');
  cameraLink.href = sample.camera;
  cameraLink.target = '_blank';
  cameraLink.rel = 'noopener noreferrer';
  container.replaceChildren(
    element('p', `Source: ${sample.source_id}`, 'sample-caption'),
    video,
    element('p', '左 A / view0，右 B / view1。视频为缩小的有损展示预览，非训练像素。', 'sample-caption'),
    metrics,
    element('p', sample.training_admission, 'admission-note'),
    conditions,
    notes,
    cameraLink,
    details,
  );
  if (sample.multi_rate) {
    const rate = element('p', `原生同视频多段变速 · ${sample.rate_min.toFixed(3)}× – ${sample.rate_max.toFixed(3)}×；浏览器仍按正常倍率播放。`, 'admission-note');
    container.insertBefore(rate, video);
  }
  if (sample.time_program) {
    const program = element('details', undefined, 'sample-details');
    program.append(element('summary', '查看时间分段 / 渐变节点与来源'), element('pre', JSON.stringify(sample.time_program, null, 2)));
    container.append(program);
  }
}

try {
  const response = await fetch('samples.json', { cache: 'no-cache' });
  if (!response.ok) throw new Error(`HTTP ${response.status}`);
  const manifest = await response.json();
  root.replaceChildren();
  for (const group of ['GTA replay', 'GTA anime', 'DL3DV']) {
    const samples = manifest.samples.filter(sample => sample.group === group);
    const section = element('section', undefined, 'sample-group');
    const heading = element('h2', `${group} · ${samples.length} 个样本`);
    const picker = element('div', undefined, 'sample-picker');
    const select = element('select');
    select.id = `sample-${group.toLowerCase().replaceAll(' ', '-')}`;
    const label = element('label', '选择样本');
    label.htmlFor = select.id;
    select.setAttribute('aria-label', `${group} 样本`);
    for (const sample of samples) {
      const option = element('option', sample.title);
      option.value = sample.id;
      select.append(option);
    }
    const content = element('div');
    select.addEventListener('change', () => renderSample(samples.find(sample => sample.id === select.value), content));
    picker.append(label, select);
    section.append(heading, picker, content);
    renderSample(samples[0], content);
    root.append(section);
  }
} catch (error) {
  root.replaceChildren(element('p', `样本加载失败：${error.message}。请刷新后重试。`, 'load-error'));
}
