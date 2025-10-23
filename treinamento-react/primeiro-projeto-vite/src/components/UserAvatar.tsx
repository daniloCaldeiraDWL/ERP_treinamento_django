export const UserAvatar = () => {
  return (
    <>
        <img 
            src="https://otempo.scene7.com/is/image/sempreeditora/super-noticia-odete-roitman-em-vale-tudo-1760062340?qlt=90&wid=1200&ts=1760076324067&dpr=off" 
            alt="Ninguém mata Odete Roitman meu bem!" 
            onClick={() => alert('Buuuum... morreu!')}
            // reduzindo o tamanho da imagem
            width={220}
            height={200}
        />
    </>
  )
}