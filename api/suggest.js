export default async function handler(req, res) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  const { type, data } = req.body;

  const botToken = process.env.TELEGRAM_BOT_TOKEN;
  const chatId = process.env.TELEGRAM_CHAT_ID || '957398801';

  if (!botToken) {
    return res.status(500).json({ error: 'Bot token not configured' });
  }

  const now = new Date().toLocaleString('vi-VN', {
    timeZone: 'Asia/Ho_Chi_Minh',
    hour12: false,
  });

  let text = '';
  if (type === 'dish') {
    text = `🍽️ **GÓP Ý MÓN MỚI**\n━━━━━━━━━━━━━━━━\n🧑 Người gửi: ${data.name || 'Ẩn danh'}\n🍖 Tên món: ${data.dishName}\n📂 Danh mục: ${data.category}\n📝 Mô tả: ${data.description || '—'}\n🕐 ${now}`;
  } else if (type === 'feature') {
    text = `💡 **ĐỀ XUẤT TÍNH NĂNG**\n━━━━━━━━━━━━━━━━\n🧑 Người gửi: ${data.name || 'Ẩn danh'}\n📌 Tiêu đề: ${data.title}\n📝 Chi tiết: ${data.description || '—'}\n🕐 ${now}`;
  } else {
    return res.status(400).json({ error: 'Invalid type' });
  }

  try {
    const url = `https://api.telegram.org/bot${botToken}/sendMessage`;
    const tgRes = await fetch(url, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        chat_id: parseInt(chatId),
        text,
        parse_mode: 'Markdown',
      }),
    });

    const tgData = await tgRes.json();

    if (!tgData.ok) {
      console.error('Telegram API error:', tgData);
      return res.status(500).json({ error: 'Failed to send message' });
    }

    return res.status(200).json({ ok: true });
  } catch (err) {
    console.error('Error:', err);
    return res.status(500).json({ error: 'Internal error' });
  }
}
