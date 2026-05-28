import os
import subprocess
import sys
from urllib.parse import urlparse

try:
    import yt_dlp
except ImportError:
    print("yt-dlp yüklü değil. Lütfen 'pip install yt-dlp' komutunu çalıştırın.")
    sys.exit(1)


def find_vlc_path():
    """Windows'ta VLC'nin kurulum yolunu bulur"""
    vlc_paths = [
        r"C:\Program Files\VideoLAN\VLC\vlc.exe",
        r"C:\Program Files (x86)\VideoLAN\VLC\vlc.exe",
        os.path.expanduser(r"~\AppData\Local\Programs\VideoLAN\VLC\vlc.exe"),
    ]
    
    for path in vlc_paths:
        if os.path.exists(path):
            return path
    
    # PATH'ta ara
    for path in os.environ.get('PATH', '').split(os.pathsep):
        vlc_path = os.path.join(path, 'vlc.exe')
        if os.path.exists(vlc_path):
            return vlc_path
    
    return None


def play_youtube_video(url, player=None):
    """
    YouTube videosunu stream edip player'da açar (indirmeden).
    
    Args:
        url (str): YouTube video URL'si
        player (str): Kullanılacak player (örn: 'vlc', 'mpv', None için sistem varsayılanı)
    """
    # yt-dlp ayarları - indirme olmadan stream URL'si al
    ydl_opts = {
        'format': 'best',  # En iyi kalite
        'quiet': False,
        'no_warnings': False,
    }
    
    print(f"Video stream ediliyor: {url}")
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Video bilgisi al (indirmeden)
            info = ydl.extract_info(url, download=False)
            video_title = info.get('title', 'video')
            stream_url = info['url']
            
        print(f"Video bulundu: {video_title}")
        
        # Player'da aç
        if player:
            # Belirli bir player kullan
            if player.lower() == 'vlc':
                if sys.platform == 'win32':
                    vlc_path = find_vlc_path()
                    if vlc_path:
                        cmd = [vlc_path, stream_url]
                    else:
                        print("VLC bulunamadı! Lütfen VLC'yi yükleyin veya player belirtmeyin.")
                        print("VLC indir: https://www.videolan.org/vlc/")
                        sys.exit(1)
                else:
                    cmd = ['vlc', stream_url]
            elif player.lower() == 'mpv':
                cmd = ['mpv', stream_url]
            else:
                cmd = [player, stream_url]
        else:
            # Sistem varsayılan player'ı kullan (stream URL'si ile)
            if sys.platform == 'win32':
                # Windows'ta varsayılan browser ile aç
                os.startfile(stream_url)
                print(f"Video varsayılan player'da açılıyor...")
                return
            elif sys.platform == 'darwin':
                cmd = ['open', stream_url]
            else:
                cmd = ['xdg-open', stream_url]
        
        subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        print(f"Video player'da açılıyor...")
        print(f"Stream URL: {stream_url}")
        
    except Exception as e:
        print(f"Hata oluştu: {e}")
        sys.exit(1)


if __name__ == "__main__":
    # Varsayılan URL
    default_url = "https://www.youtube.com/watch?v=ETad6kkfw2o&pp=0gcJCQ0LAYcqIYzv"
    
    # Komut satırı argümanlarını kontrol et
    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        url = default_url
    
    # Player seçimi (opsiyonel)
    player = None
    if len(sys.argv) > 2:
        player = sys.argv[2]
    
    # URL doğrulama
    parsed = urlparse(url)
    if not all([parsed.scheme, parsed.netloc]):
        print("Geçersiz URL!")
        sys.exit(1)
    
    play_youtube_video(url, player)
