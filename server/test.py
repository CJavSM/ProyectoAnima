import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

load_dotenv()

print("=" * 50)
print("PRUEBA DE CONEXIÓN CON SPOTIFY")
print("=" * 50)

client_id = os.getenv('SPOTIFY_CLIENT_ID')
client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')

print(f"\n1. Verificando credenciales:")
print(f"   Client ID: {client_id[:10]}..." if client_id else "   ❌ Client ID no encontrado")
print(f"   Client Secret: {client_secret[:10]}..." if client_secret else "   ❌ Client Secret no encontrado")

if not client_id or not client_secret:
    print("\n❌ ERROR: Credenciales de Spotify no configuradas")
    exit(1)

print("\n2. Intentando autenticar con Spotify...")
try:
    auth_manager = SpotifyClientCredentials(
        client_id=client_id,
        client_secret=client_secret
    )
    sp = spotipy.Spotify(auth_manager=auth_manager)
    print("   ✅ Autenticación exitosa")
except Exception as e:
    print(f"   ❌ Error en autenticación: {str(e)}")
    exit(1)

print("\n3. Probando búsqueda simple...")
try:
    results = sp.search(q='happy upbeat party', type='track', limit=5, market='US')
    
    print(f"   ✅ Búsqueda exitosa")
    print(f"   Canciones encontradas: {len(results['tracks']['items'])}")
    
    if results['tracks']['items']:
        print("\n4. Ejemplos de canciones:")
        for i, track in enumerate(results['tracks']['items'][:3], 1):
            print(f"   {i}. {track['name']} - {track['artists'][0]['name']}")
    
except Exception as e:
    print(f"   ❌ Error en búsqueda: {str(e)}")
    import traceback
    traceback.print_exc()
    exit(1)

print("\n5. Probando búsqueda con filtros de año y género...")
try:
    query = "happy upbeat party year:2015-2024 genre:pop"
    results = sp.search(q=query, type='track', limit=10, market='US')
    
    print(f"   ✅ Búsqueda con filtros exitosa")
    print(f"   Canciones encontradas: {len(results['tracks']['items'])}")
    
    if results['tracks']['items']:
        print("\n6. Top 3 canciones más populares:")
        sorted_tracks = sorted(results['tracks']['items'], key=lambda x: x['popularity'], reverse=True)
        for i, track in enumerate(sorted_tracks[:3], 1):
            print(f"   {i}. {track['name']} - {track['artists'][0]['name']} (Popularidad: {track['popularity']})")
    
except Exception as e:
    print(f"   ❌ Error: {str(e)}")
    import traceback
    traceback.print_exc()

print("\n7. Probando múltiples búsquedas (simulando emociones)...")
try:
    emotions_queries = {
        'HAPPY': 'happy upbeat party',
        'SAD': 'sad emotional melancholic',
        'CALM': 'calm relaxing peaceful'
    }
    
    for emotion, query in emotions_queries.items():
        results = sp.search(q=query, type='track', limit=5, market='US')
        print(f"   {emotion}: {len(results['tracks']['items'])} canciones encontradas")
    
    print("   ✅ Todas las búsquedas exitosas")
    
except Exception as e:
    print(f"   ❌ Error: {str(e)}")

print("\n" + "=" * 50)
print("✅ PRUEBA COMPLETADA EXITOSAMENTE")
print("=" * 50)
print("\nAhora puedes reiniciar el servidor:")
print("  python main.py")