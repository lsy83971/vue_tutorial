<template>
  <div id="about_total">
  <article>
    <h1>overview</h1>
    <p>
      JSM is an mind-map editor,
    </p>
    <p>
      Futhermore, it's a data-pipeline developing environment(based on Python3).
    </p>
    <p>
      The server will create an python backend to execute code and save the data.
    </p>
  </article>
  <article>
    <h1>data-pipeline</h1>
    <p>
      Pipeline is consist of nodes and pipes
    </p>
    <h3>
      pipe
    </h3>
    <p>
      pipes defines who's the parent and who's the child.

    </p>
    <p>
      when pipes link two nodes together. the one on the left is parent, and the one on the right is child
    </p>
    <h3>
      node
    </h3>
    <p>
      Node receives data from its parent, and execute some code, then produce the target data and pass it to its children
    </p>
    <p>
      there is a special node called 'root' node, it is the only node that don't have a parent, and cannot be removed
    </p>
    <p>
      only root node receives the source data, the others receives data from parent.
    </p>
    <p>
      after running the pipeline, the data of all nodes will be recorded and shown in the result block 
    </p>
  </article>
  
  <article>
    <h1>get started</h1>
    <p>
      Just do 3 things, you can start the pipeline:
    </p>
    <p>      	
      1.give source data; 2.edit the pipeline; 3.click the 'run' button;
    </p>	
    <p>      
      you can do the editing, executing, debugging in the same window.
    </p>
    <p>
      and there are planty of shortcuts and navigator, that make the coding and debugging quite convience.
    </p>
    <h3>
      editing pipeline
    </h3>

    <p>
      click on any node then press ESC, you may find that editing is prevented, and the block turn red. that means you enter function mode.
    </p>
    <p>
      under function mode all the input turn into functional.
    </p>
    <p>
      press a: create a child node
    </p>
    <p>
      press s: create a surfix node
    </p>
    <p>
      press ctrl+up: move up
    </p>
    <p>
      press ctrl+down: move down etc...
    </p>
    <p>
      you can find the all the functional in <a>shortcut list</a>
    </p>
    <p>
      when press space, you can exit function mode and start editing.
    </p>
    <h3>
      editing node
    </h3>
    <p>
      you can editing the code like python editor
    </p>
    <p>
      there are 6 type of node:raw, as, copy, iter, null, off,
      the nodetype was typed on the first line of the block
    </p>
    <p>
      first you need to know about raw, just bare in mind a few things:
    </p>
    <p>
      1. the basic task of a node is to produce the data
      2. $f(f short for from) is the data from parent(for root node, $f is the source data)
      3. $t is your target
    </p>
    <h3>
      here are some node examples:
    </h3>
    <p>
      example1: give what receive from the parent
    </p>
    <textarea cols="30">
      raw
      $t=$f
    </textarea>
    <p>
      example2: receive n and pass n+1
    </p>
    <textarea cols="30">
      raw
      $t=$f+1
    </textarea>
    <p>
      example3: receive a list and pass the first element of a list
    </p>
    <textarea cols="30">
      raw
      $t=$f[0]
    </textarea>
    <p>
      example4: no matter what the node receive, just pass 1
    </p>
    <textarea cols="30">
      raw
      $t=1;
    </textarea>
    <p>
      example5: very simple pipeline;node1 returns3;node2 returns4;node3 returns6;
    </p>
    <img alt="Vue logo" src="../assets/pipeline_example1.png">
    <h3>more types: 'as' and 'copy'</h3>
    <p>'as' and 'copy' make very tiny difference from 'raw'
    </p>
    <p>in 'as' type, you just give a expression, then it will automaticly pass it to $t.
    </p>
    <p>example for 'as':</p>
    <textarea cols="30">
      as
      $f+1
    </textarea>
    <p>
      is the same as 
    </p>
    <textarea cols="30">
      raw
      $t=$f+1
    </textarea>
    <p>in 'copy' type, you just give make some change to $f and, then it will automaticly pass $f to $t.
    </p>
    <p>Important the change on $t will also change the parent data, if the data's type is not simple type. and that's very useful.
    </p>
    <p>example for 'copy':</p>
    <textarea cols="30">
      copy
      $f['a']=1
    </textarea>
    <p>
      is the same as 
    </p>
    <textarea cols="30">
      raw
      $f['a']=1
      $t=$f
    </textarea>
    <h3>Global var: $g</h3>
    <p>In ordinary situation, in a node's view, the only information you know is the data that received from parent</p>    
    <p>But under some complecated circumstance, you may want to pass information from one node to another that is not under relationship of child and parent</p>
    <p>To deal with these problems. We have $g as global inventory, every nodes can see $g</p>
    <p>you can use $g.helloWorld="Hello World" in one node</p>
    <p>and receive "Hello World" with $g.helloWorld in any other node that is executed after that</p>

    <h3>'null' type</h3>
    <p>just execute code but don't pass data to the child</p>
    <p>that means all its children and descendant won't receive data and give no output</p>

    <h3>'off' type</h3>
    <p>like null but do not execute code and do not pass data either</p>

    <h3>'iter' type</h3>
    <p>coming soon </p>
  </article>
  <article>
    <h1>Button</h1>
    <p>
      run: run the pipeline
    </p>
    <p>
      clear: clear the pipeline
    </p>
    <p>
      revert: when you leave the page, and with web-session still on, you can reload the page and recover the tree.
    </p>
  </article>
  <article>
    <h1>shortcut</h1>
    <h3>Under function mode</h3>
    <p>
      a:add node
    </p>      
    <p>
      s:add surfix node
    </p>      
    <p>
      tab: fold or unfold node
    </p>      
    <p>
      d or delete:delete node
    </p>      
    <p>
      c: copy node
    </p>      
    <p>
      p: paste node (with all children and surfix)
    </p>      
    <p>
      g: goto result
    </p>      
    <p>
      t: get into context of this node
    </p>      
    <p>
      Ctrl+up: move up
    </p>      
    <p>
      Ctrl+down: move down      
    </p>
  </article>
  <article>
    <h1>code editor</h1>
    <p>
      $fd: fromdataDict
    </p>
    <p>
      $td: todataDict
    </p>
    <p>
      $f: fromdata
    </p>
    <p>
      $t: todata
    </p>
    <p>
      $n: temp node under context
    </p>
    <p>
      $nd: nodeDict
    </p>
    <p>
      $g: global inventory
    </p>
  </article>
</div>  
</template>
<style>
  #about_total {
  padding-left:50px;
  padding-right:50px;  
  }
  p {
  text-align:left;
  }
  h1 {
  text-align:left;
  }
  h2 {
  text-align:left;
  }
  h3 {
  text-align:left;
  }
  
</style>  
