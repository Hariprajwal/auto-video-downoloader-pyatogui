import pyautogui
import pyperclip
import time
import webbrowser
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import platform
import subprocess

def extract_urls_from_input(user_input):
    """
    Extract multiple URLs from user input using space or comma separation
    AND handle continuous links without separators
    """
    urls = []
    
    # First, try to find URLs using regex pattern
    url_pattern = r'https?://[^\s,]+'
    found_urls = re.findall(url_pattern, user_input)
    
    if found_urls:
        # If regex found URLs, use them
        urls = found_urls
    else:
        # Fallback: split by both commas and spaces
        raw_urls = re.split(r'[,\s]+', user_input)
        
        for url in raw_urls:
            url = url.strip()
            # Basic URL validation
            if url and (url.startswith('http://') or url.startswith('https://')):
                urls.append(url)
    
    return urls

def setup_browser():
    """Setup Chrome browser with appropriate options"""
    try:
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        driver = webdriver.Chrome(options=chrome_options)
        return driver
    except Exception as e:
        print(f"❌ Chrome driver setup failed: {e}")
        print("💡 Please ensure ChromeDriver is installed and in PATH")
        return None

def open_downloader_tab(driver, video_number, total_videos):
    """Open new tab with downloader website"""
    print(f"📱 Opening downloader tab for video {video_number}/{total_videos}...")
    
    try:
        # Open new tab
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[-1])
        
        # Navigate to downloader website
        driver.get("https://savefrom.in.net/en7/youtube-video-downloader")
        
        print("✅ Downloader website opened")
        time.sleep(3)
        return True
        
    except Exception as e:
        print(f"❌ Failed to open downloader tab: {e}")
        return False

def paste_video_link(video_url):
    """Click on coordinates and paste video link"""
    print("🖱 Clicking on input field (570, 491)...")
    
    try:
        # Click on input field coordinates
        pyautogui.click(547, 447)
        time.sleep(1)
        
        # Select all and paste the video URL
        pyautogui.hotkey('ctrl', 'a')
        pyperclip.copy(video_url)
        pyautogui.hotkey('ctrl', 'v')
        
        print("✅ Video link pasted successfully")
        return True
        
    except Exception as e:
        print(f"❌ Failed to paste video link: {e}")
        return False

def wait_and_click_download():
    """Wait 15 seconds and click download button"""
    print("⏳ Waiting 15 seconds for processing...")
    time.sleep(15)
    
    print("🖱 Clicking download button (1452, 514)...")
    try:
        pyautogui.click(1470, 482)
        print("✅ Download button clicked")
        return True
    except Exception as e:
        print(f"❌ Failed to click download button: {e}")
        return False

def wait_and_select_format():
    """Wait 5 seconds and select download format"""
    print("⏳ Waiting 5 seconds for format options...")
    time.sleep(15)
    
    print("🖱 Selecting download format (929, 534)...")
    try:
        pyautogui.click(929, 534)
        print("✅ Format selected")
        return True
    except Exception as e:
        print(f"❌ Failed to select format: {e}")
        return False

def wait_for_download_completion():
    """Wait 10 seconds for download to complete"""
    print("⏳ Waiting 10 seconds for download completion...")
    time.sleep(10)
    print("✅ Download process completed")

def close_current_tab(driver):
    """Close current tab and switch back to main window"""
    try:
        driver.close()
        if len(driver.window_handles) > 0:
            driver.switch_to.window(driver.window_handles[0])
        print("✅ Tab closed")
        return True
    except Exception as e:
        print(f"❌ Failed to close tab: {e}")
        return False

def process_single_video(driver, video_url, video_number, total_videos):
    """Process single video download with all steps"""
    print(f"\n{'='*60}")
    print(f"🎬 PROCESSING VIDEO {video_number} OF {total_videos}")
    print(f"🔗 URL: {video_url}")
    print(f"{'='*60}")
    
    # Step 1: Open downloader tab
    if not open_downloader_tab(driver, video_number, total_videos):
        return False
    
    # Step 2: Paste video link
    if not paste_video_link(video_url):
        return False
    
    # Step 3: Wait and click download
    if not wait_and_click_download():
        return False
    
    # Step 4: Wait and select format
    if not wait_and_select_format():
        return False
    
    # Step 5: Wait for download completion
    wait_for_download_completion()
    
    # Step 6: Close current tab
    if not close_current_tab(driver):
        return False
    
    print(f"🎉 Video {video_number} processed successfully!")
    return True

def display_warning():
    """Display important warning messages"""
    print("⚠️  IMPORTANT WARNINGS:")
    print("   • DO NOT move mouse or use keyboard during automation")
    print("   • Ensure screen resolution is 1920x1080")
    print("   • Keep browser window focused")
    print("   • Make sure Chrome browser is installed")
    print("   • Downloads will go to your default download folder")
    print()

def main():
    """Main function to run the video downloader"""
    print("🎥 AUTOMATED VIDEO DOWNLOADER")
    print("=" * 50)
    
    # Display warnings
    display_warning()
    
    # Get video links from user
    video_links_input = input("Paste video URL(s) (separated by spaces or commas) and press Enter: ").strip()

    if not video_links_input:
        print("❌ No URLs provided. Exiting.")
        return

    # Extract multiple URLs from input
    ALL_VIDEO_URLS = extract_urls_from_input(video_links_input)
    
    if not ALL_VIDEO_URLS:
        print("❌ No valid URLs found. Please provide valid video links.")
        return
    
    print(f"📋 Found {len(ALL_VIDEO_URLS)} video URL(s) to process:")
    for i, url in enumerate(ALL_VIDEO_URLS):
        print(f"  {i+1}. {url}")
    
    # Setup browser
    print("\n🚀 Setting up browser...")
    driver = setup_browser()
    
    if not driver:
        print("❌ Browser setup failed. Exiting.")
        return
    
    try:
        # Open initial tab
        driver.get("https://www.google.com")
        
        print(f"\n⏳ Starting download process for {len(ALL_VIDEO_URLS)} videos in 5 seconds...")
        print("⚠️  DO NOT TOUCH MOUSE OR KEYBOARD!")
        
        # Countdown
        for i in range(5, 0, -1):
            print(f"Starting in {i} seconds...")
            time.sleep(1)
        
        print("🎬 Automation STARTED!")
        
        # Safety settings for pyautogui
        pyautogui.FAILSAFE = True
        
        # Process each video
        successful_downloads = 0
        
        for i, video_url in enumerate(ALL_VIDEO_URLS, 1):
            if process_single_video(driver, video_url, i, len(ALL_VIDEO_URLS)):
                successful_downloads += 1
            
            # Wait before processing next video (if any remaining)
            if i < len(ALL_VIDEO_URLS):
                print(f"\n⏳ Preparing for next video in 3 seconds...")
                time.sleep(3)
        
        # Final summary
        print(f"\n{'='*60}")
        print("📊 PROCESSING SUMMARY")
        print(f"{'='*60}")
        print(f"✅ Successfully processed: {successful_downloads}/{len(ALL_VIDEO_URLS)} videos")
        print(f"❌ Failed: {len(ALL_VIDEO_URLS) - successful_downloads}/{len(ALL_VIDEO_URLS)} videos")
        print("🎉 All operations completed!")
        
    except KeyboardInterrupt:
        print("\n🛑 Process interrupted by user!")
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")
    finally:
        if driver:
            print("\nClosing browser...")
            driver.quit()
        print("Program finished.")

# Required installation instructions
def show_installation_instructions():
    """Show package installation instructions"""
    print("\n📦 REQUIRED INSTALLATION:")
    print("Run these commands in your terminal/command prompt:")
    print("pip install selenium pyautogui pyperclip")
    print("\nAlso download ChromeDriver from: https://chromedriver.chromium.org/")
    print("And ensure it's in your system PATH")

if __name__ == "__main__":
    # Show installation instructions if needed
    show_installation_instructions()
    print("\n" + "="*50)
    
    # Run main program
    main()
