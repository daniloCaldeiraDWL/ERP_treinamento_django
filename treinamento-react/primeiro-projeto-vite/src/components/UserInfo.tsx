// importação dos componentes
import { UserName } from './UserName'
import { UserEmail } from './UserEmail'
import { UserAge } from './UserAge'
import { UserAvatar } from './UserAvatar'

export const UserInfo = () => {
  return (
    <>
      <UserAvatar />
      <UserName />
      <UserEmail />
      <UserAge />
    </>
  )
}