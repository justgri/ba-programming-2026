document.addEventListener('DOMContentLoaded', async () => {
  // Map: CSS class -> Path to the ES module
  const scriptMapping = {
    'js-tableFilter': './table-filter.js',
  };

  for (const [cssClass, modulePath] of Object.entries(scriptMapping)) {
    // Check if the current page contains an element with this class
    if (document.querySelector(`.${cssClass}`)) {
      try {
        // Dynamically import the module
        const importedModule = await import(modulePath);

        // If the module has an init function (or any function you want to call),
        // call it here. (Use the actual exported name from that module.)
        if (typeof importedModule.initTableFilters === 'function') {
          importedModule.initTableFilters();
        }
      } catch (err) {
        console.error(`Failed to load module: ${modulePath}`, err);
      }
    }
  }
});
