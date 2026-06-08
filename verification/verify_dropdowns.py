import asyncio
from playwright.async_api import async_playwright
import os

async def verify():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        context = await browser.new_context(viewport={'width': 1280, 'height': 800})
        page = await context.new_page()

        # Go to the simulation page
        await page.goto("http://localhost:8502")
        # Wait for the main shell to appear
        try:
            await page.wait_for_selector(".st-key-dashboard_shell", timeout=20000)
        except:
            print("Dashboard shell not found, taking debug screenshot")
            await page.screenshot(path="verification/screenshots/timeout_debug.png")
            await browser.close()
            return

        await page.wait_for_timeout(5000) # Wait for animations

        # 1. WDM channel number selection
        selectbox_wdm = page.locator("[data-testid='stSelectbox']").filter(has_text="WDM channels")
        await selectbox_wdm.scroll_into_view_if_needed()
        await selectbox_wdm.locator("div[data-baseweb='select']").click()
        await page.wait_for_timeout(1000)
        await page.screenshot(path="verification/screenshots/wdm_dropdown.png")
        await page.keyboard.press("Escape")

        # 2. Rate selection - Corrected label
        selectbox_rate = page.locator("[data-testid='stSelectbox']").filter(has_text="Rate / channel (Gbps)")
        await selectbox_rate.scroll_into_view_if_needed()
        await selectbox_rate.locator("div[data-baseweb='select']").click()
        await page.wait_for_timeout(1000)
        await page.screenshot(path="verification/screenshots/rate_dropdown.png")
        await page.keyboard.press("Escape")

        # 3. Scenario detail selection
        # Need to run benchmarks first
        run_benchmarks = page.get_by_role("button", name="Run benchmarks")
        await run_benchmarks.click()
        print("Clicked Run benchmarks, waiting...")
        # Increased wait for benchmarks
        await page.wait_for_timeout(20000)

        # Go to Scenario detail tab
        scenario_tab = page.get_by_role("tab", name="Scenario detail")
        if await scenario_tab.count() > 0:
            await scenario_tab.click()
            await page.wait_for_timeout(2000)

            # Selectbox in scenario detail
            scenario_selectbox = page.locator("[data-testid='stSelectbox']").filter(has_text="Scenario detail")
            await scenario_selectbox.locator("div[data-baseweb='select']").click()
            await page.wait_for_timeout(1000)
            await page.screenshot(path="verification/screenshots/scenario_dropdown.png")
        else:
            print("Scenario detail tab not found")
            await page.screenshot(path="verification/screenshots/no_tab_debug.png")

        await browser.close()

if __name__ == "__main__":
    asyncio.run(verify())
