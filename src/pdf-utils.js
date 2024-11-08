// Load html2canvas and DOMPurify

import jsPDF from "jspdf";


export async function string_to_pdf(htmlString, config = {}) {
  config = {
    ...{
      orientation: "portrait",
      unit: "pt",
      format: "a4",
      width: "800px",
      height: "850px",
    },
    ...config,
  };
  const { width, height } = config;
  delete config.width;
  delete config.height;
  console.log(config);
  // Create an overlay to hide the process
  const overlay = document.createElement("div");
  overlay.innerHTML = `
    <div style="
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      background-color: rgba(0, 0, 0, 1);
      z-index: 1000;
      display: flex;
      justify-content: center;
      align-items: center;
      color: white;
      font-size: 24px;
    ">
      Generating PDF, please wait...
    </div>
  `;
  document.body.appendChild(overlay);
  await new Promise((resolve) => setTimeout(resolve, 100)); // Wait for the overlay to render

  // Create a temporary container and set its inner HTML
  const iframe = document.createElement("iframe");
  iframe.style.position = "absolute";
  iframe.style.top = "-9999px"; // Hide the iframe offscreen
  document.body.appendChild(iframe);

  const iframeDoc = iframe.contentDocument || iframe.contentWindow.document;
  iframeDoc.open();
  iframeDoc.write(htmlString);
  iframeDoc.close();

  const container = iframeDoc.documentElement;
  console.log(container);

  // Load jsPDF
  const pdf = new jsPDF(config);

  // Calculate scale to fit content to PDF page
  const pageWidth = pdf.internal.pageSize.getWidth();
  const pageHeight = pdf.internal.pageSize.getHeight();
  // Set the iframe width and height to the PDF page dimensions
  iframe.style.width = `${width}`;
  iframe.style.height = `${height}`;
  console.log(pageWidth);
  console.log(container.offsetWidth);

  // container.style.overflow = "hidden"; // Hide overflow content

  const contentWidth = container.offsetWidth;
  const contentHeight = container.offsetHeight;

  // Calculate scale factors for both dimensions
  const scaleX = pageWidth / contentWidth;
  const scaleY = pageHeight / contentHeight;
  const scale = Math.min(scaleX, scaleY); // Choose the smaller scale to fit content

  console.log(scale);
  // Remove all CSS links
  const cssLinks = Array.from(
    document.querySelectorAll('link[rel="stylesheet"]')
  );
  cssLinks.forEach((link) => link.parentNode.removeChild(link));

  // Use the container with pdf.html()
  await pdf.html(container, {
    callback: async function (pdf) {
      pdf.save("document.pdf"); // Save the generated PDF

      // Add back all CSS links
      cssLinks.forEach((link) => document.head.appendChild(link));

      // Remove the overlay after PDF generation
      document.body.removeChild(iframe);
      await new Promise((resolve) => setTimeout(resolve, 100)); // Wait for the overlay to render
      document.body.removeChild(overlay);
    },
    html2canvas: { scale: scale }, // Apply calculated scale
  });

  // Clean up the temporary container
}
