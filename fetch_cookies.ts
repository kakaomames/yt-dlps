import puppeteer from "https://deno.land/x/puppeteer/mod.ts";

const browser = await puppeteer.launch({ headless: "new" });
const page = await browser.newPage();

// YouTubeにアクセス（ユーザーエージェントをGalaxy S25に偽装）
await page.setUserAgent("Mozilla/5.0 (Linux; Android 15; SM-S931N) ...");
await page.goto("https://www.youtube.com");

// クッキーを抽出して Netscape 形式に変換
const cookies = await page.cookies();
let cookieStr = "# Netscape HTTP Cookie File\n";
for (const c of cookies) {
  cookieStr += `${c.domain}\tTRUE\t/\t${c.secure}\t0\t${c.name}\t${c.value}\n`;
}

await Deno.writeTextFile("cookies.txt", cookieStr);
await browser.close();
