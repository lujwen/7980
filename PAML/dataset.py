import datetime
import pandas as pd
import math

class dbook(object):
    def __init__(self):
        self.rating_data, self.user_feature, self.item_feature, self.user_user, self.rating_list = self.load()
        self.user_neighbor = self.get_neighbor()
        #modifying
        self.user_groups_list = self.get_user_groups_list()
        # self.user_power_score = self.get_user_power_score(base_groups = 2, base_score = 1.5, k = 1)
        # self.user_power_score = self.get_user_power_score()
        self.all_groups_list = self.get_all_groups_list()
        self.user_group_list = self.get_user_group_list()
        #end modifying

    def load(self):
        input_dir = "data/dbook/original/"

        rating_data = pd.read_csv(input_dir + 'user_book.dat', names=['user', 'item', 'rating'], sep='\t', engine='python')

        rating_list = sorted(list(rating_data['rating'].unique()))
        print('rating types in user_book: %s' % len(rating_list))

        ul = pd.read_csv(input_dir + 'user_location.dat', names=['user', 'location'], sep='\t', engine='python')
        print('users in user_location: %s' % len(ul['user'].unique()))
        ug = pd.read_csv(input_dir + 'user_group.dat', names=['user', 'group'], sep='\t', engine='python')
        print('users in user_group: %s' % len(ug['user']))
        #modifying 
        user_groups_list = pd.read_csv(input_dir + 'uniq_user_groups.dat', names=['user', 'groups'], sep='\t', engine='python')
        print('uniq user in groups: %s' % len(user_groups_list['user']))
        # end modifying

        user_feature = ul
        print('user in user_feature: %s' % len(user_feature['user'].unique()))

        ba = pd.read_csv(input_dir + 'book_author.dat', names=['item', 'author'], sep='\t', engine='python')
        print('books in book_author: %s' % len(ba['item'].unique()))
        bp = pd.read_csv(input_dir + 'book_publisher.dat', names=['item', 'publisher'], sep='\t', engine='python')
        print('books in book_publisher: %s' % len(bp['item'].unique()))
        by = pd.read_csv(input_dir + 'book_year.dat', names=['item', 'year'], sep='\t', engine='python')
        print('books in book_year: %s' % len(by['item'].unique()))
        item_feature = pd.merge(ba, bp, on='item')
        print('books in book_feature: %s' % len(item_feature['item'].unique()))

        user_user = pd.read_csv(input_dir + 'user_user.dat', names=['user1', 'user2'], sep='\t', engine='python')
        
        return rating_data, user_feature, item_feature, user_user, rating_list
    

    def get_neighbor(self): # friends
        user_neighbor = dict()
        for _, (row) in self.user_user.iterrows():
            user1 = row['user1']
            user2 = row['user2']
            if user1 not in user_neighbor:
                user_neighbor[user1] = []
            if user2 not in user_neighbor:
                user_neighbor[user2] = []
            user_neighbor[user1].append(user2)
            user_neighbor[user2].append(user1)
        return user_neighbor
    
# # modifying
# data process, return a dictionary containing user:groups  {user1: [g1, g2, g3], user2: [g1, g2, g3]}
    def get_user_groups_list(self):
        input_dir = "data/dbook/original/"
        user_groups = pd.read_csv(input_dir + 'user_group.dat', names=['user', 'group'], sep='\t', engine='python')
        # user_groups_pair = user_groups.groupby('user')['group'].apply(list).reset_index()
        # user_groups_list = list(user_groups_pair.itertuples(index=False, name=None))
        user_groups_list = user_groups.groupby('user')['group'].apply(list).to_dict()
        return user_groups_list # dictionary  {user1: [g1, g2, g3], user2: [g1, g2, g3]}
    
# data process, return all groups list [group1, group2 ....]
    def get_all_groups_list(self):
        input_dir = "data/dbook/original/"
        ug = pd.read_csv(input_dir + 'user_group.dat', names=['user', 'group'], sep='\t', engine='python')
        all_group_list = ug['group'].unique().tolist()
        return all_group_list # [group1, group2 ....]
    
# data process, return a list containing user：group pairs [(user1, group1), (user2, group2)]  
    def get_user_group_list(self):
        input_dir = "data/dbook/original/"
        ug = pd.read_csv(input_dir + 'user_group.dat', names=['user', 'group'], sep='\t', engine='python')
        user_group_list = list(zip(ug['user'], ug['group']))
        return user_group_list # [(user1, group1), (user2, group2)]

        
    # def get_user_power_score(self, base_groups, base_score, k): 
    # def get_user_power_score(self): 
    #     # k = math.ceil(len(self.ugs['user']) * 0.25) # k = top i power users
    #     # power_users = []
    #     # for user, _ in self.ugs.iterrows():
    #     #     power_users.append(user)
    #     #     k -= 1
    #     #     if k == 0:
    #     #         break
    #     # user_groups: {1:[g1, g2, g3]}
    #     user_power_score = dict()
    #     total_groups = self.get_total_user_group()
    #     for user, groups in self.user_groups_list.iterrows():
    #         user_power_score[user] = len(groups) / len(total_groups)
    #         # add_score = math.ceil((len(groups) - base_groups) / k)
    #         # user_power_score[user] = base_score * (1 + add_score * 0.1)     
    #     return user_power_score   
    
    #{1: 2.5} 
            
# #end modifying 


class yelp(object):
    def __init__(self):
        self.rating_data, self.user_feature, self.item_feature, self.rating_list = self.load()
        self.user_neighbor = self.get_neighbor()

    def load(self):
        input_dir = "data/yelp/original/"

        rating_data = pd.read_csv(input_dir + 'rating.dat', names=['user', 'item', 'rating', 'time'], sep='\t', engine='python')
        rating_data = rating_data.drop(columns=['time'])

        rating_list = sorted(list(rating_data['rating'].unique()))
        print('rating types in yelp: %s' % len(rating_list))

        uf = pd.read_csv(input_dir + 'user_fans.dat', names=['user', 'fans'], sep='\t', engine='python')
        print('users in user_fan: %s' % len(uf['user'].unique()))
        ua = pd.read_csv(input_dir + 'user_avgrating.dat', names=['user', 'avgrating'], sep='\t', engine='python')
        print('users in user_avgrating: %s' % len(ua['user']))
        user_feature = pd.merge(uf, ua, on='user')
        print('user in user_feature: %s' % len(user_feature['user'].unique()))

        i_s = pd.read_csv(input_dir + 'item_stars.dat', names=['item', 'stars'], sep='\t', engine='python')
        print('items in item_stars: %s' % len(i_s['item'].unique()))
        i_p = pd.read_csv(input_dir + 'item_postalcode.dat', names=['item', 'postalcode'], sep='\t', engine='python')
        print('items in item_postalcode: %s' % len(i_p['item'].unique()))
        item_feature = pd.merge(i_s, i_p, on='item')
        print('item in item_feature: %s' % len(item_feature['item'].unique()))

        return rating_data, user_feature, item_feature, rating_list

    def get_neighbor(self):
        user_neighbor = dict()
        with open("data/yelp/original/user_friends.dat") as fin:
            for line in fin:
                data = line.strip().split('\t')
                if len(data) != 2:
                    continue
                user1 = int(data[0])
                user2s = list(map(int, data[1].split()))
                user_neighbor[user1] = user2s
        return user_neighbor


if __name__ == '__main__':
    dbook()
    # yelp()
