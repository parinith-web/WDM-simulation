import asyncio
from playwright.async_api import async_playwright
import os

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        # Increase timeout for streamlit to load
        await page.goto("http://localhost:8501", timeout=60000)

        # Wait for the simulation section to be visible
        # Assuming the "Simulation" navigation item is clicked or it's the default
        # Based on the screenshot provided in the prompt, it seems we are on Simulation page

        # Wait for some content to load
        await page.wait_for_selector("text=Optical Secure WDM Simulator", timeout=20000)

        # Take screenshot of the main section
        await page.screenshot(path="verification/simulation_main.png")

        # Try to expand "Advanced transmitter parameters"
        # Based on screenshot, it's an expander
        try:
            await page.click("text=Advanced transmitter parameters", timeout=5000)
            await asyncio.sleep(1) # Wait for animation
            await page.screenshot(path="verification/advanced_params_expanded.png")
        except Exception as e:
            print(f"Could not expand: {e}")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(run())
